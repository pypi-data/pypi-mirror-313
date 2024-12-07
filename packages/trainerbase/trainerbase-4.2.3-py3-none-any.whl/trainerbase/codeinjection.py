from abc import ABC, abstractmethod
from contextlib import suppress
from pathlib import Path
from subprocess import DEVNULL
from subprocess import run as run_executable
from tempfile import TemporaryDirectory
from typing import ClassVar, Final, Self, override

from pymem.exception import MemoryWriteError

from trainerbase.memory import ARCH, ConvertibleToAddress, allocate, ensure_address
from trainerbase.process import pm


FASM_EXECUTABLE_PATH: Final[Path] = Path(__file__).resolve().parent.parent / "trainerbase_vendor" / "FASM.EXE"


type Code = bytes | str


class AbstractCodeInjection(ABC):
    created_code_injections: ClassVar[list[Self]] = []

    def __new__(cls, *_args, **_kwargs):
        instance = super().__new__(cls)
        AbstractCodeInjection.created_code_injections.append(instance)

        return instance

    @abstractmethod
    def inject(self):
        pass

    @abstractmethod
    def eject(self):
        pass


class CodeInjection(AbstractCodeInjection):
    def __init__(
        self,
        address: ConvertibleToAddress,
        code_to_inject: Code,
    ):
        self.address = ensure_address(address)
        self.code_to_inject = compile_asm(code_to_inject)
        self.original_code: bytes = b""
        self.injection_point: int = 0
        self._injected = False

    @override
    def inject(self):
        self.injection_point = self.address.resolve()

        self.original_code = pm.read_bytes(self.injection_point, len(self.code_to_inject))
        pm.write_bytes(self.injection_point, self.code_to_inject, len(self.code_to_inject))
        self._injected = True

    @override
    def eject(self):
        if self._injected:
            pm.write_bytes(self.injection_point, self.original_code, len(self.original_code))
            self._injected = False


class AllocatingCodeInjection(AbstractCodeInjection):  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        address: ConvertibleToAddress,
        code_to_inject: Code,
        *,
        original_code_length: int = 0,
        new_memory_size: int = 1024,
        is_long_x64_jump_needed: bool | None = None,
    ):
        if is_long_x64_jump_needed is None:
            is_long_x64_jump_needed = pm.is_64_bit

        self.is_long_x64_jump_needed = is_long_x64_jump_needed
        self.address = ensure_address(address)
        self.code_to_inject = compile_asm(code_to_inject)

        if self.is_long_x64_jump_needed:
            self.code_to_inject = compile_asm("pop rax") + self.code_to_inject + compile_asm("push rax")

        self.original_code: bytes = b""

        self.original_code_length = original_code_length
        self.new_memory_size = new_memory_size
        self.new_memory_address: int = 0
        self.injection_point: int = 0

    @override
    def inject(self):
        self.injection_point = self.address.resolve()

        self.new_memory_address: int = allocate(self.new_memory_size)

        self.original_code = pm.read_bytes(self.injection_point, self.original_code_length)

        if self.is_long_x64_jump_needed:
            jump_to_new_mem = compile_asm(get_long_x64_jump_to_new_mem_code(self.new_memory_address))
            jumper_length = len(jump_to_new_mem)
            jump_back_address = self.injection_point + jumper_length - 1
            jump_back = compile_asm(get_long_x64_jump_back_code(jump_back_address))
        else:
            jump_to_new_mem = compile_asm(get_simple_jump_code(self.new_memory_address, self.injection_point))
            jumper_length = len(jump_to_new_mem)
            jump_back_address = self.injection_point + jumper_length
            jump_back = compile_asm(
                get_simple_jump_code(jump_back_address, self.new_memory_address + len(self.code_to_inject)),
            )

        if jumper_length < self.original_code_length:
            jump_to_new_mem += b"\x90" * (self.original_code_length - len(jump_to_new_mem))
        elif jumper_length > self.original_code_length:
            raise ValueError(f"Jumper length > original code length: {jumper_length} > {self.original_code_length}")

        code_to_inject = self.code_to_inject + jump_back

        pm.write_bytes(self.new_memory_address, code_to_inject, len(code_to_inject))
        pm.write_bytes(self.injection_point, jump_to_new_mem, len(jump_to_new_mem))

    @override
    def eject(self):
        if self.new_memory_address and self.injection_point:
            pm.write_bytes(self.injection_point, self.original_code, self.original_code_length)
            pm.free(self.new_memory_address)
            self.new_memory_address = 0
            self.injection_point = 0


class MultipleCodeInjection(AbstractCodeInjection):
    def __init__(self, *injections: AbstractCodeInjection):
        self._injections = injections

    @override
    def inject(self):
        for injection in self._injections:
            injection.inject()

    @override
    def eject(self):
        for injection in self._injections:
            injection.eject()


def compile_asm(code: Code) -> bytes:
    if isinstance(code, str):
        fasm_mode = f"use{ARCH}"
        with TemporaryDirectory() as tmp_dir:
            asm_file = Path(tmp_dir) / "injection.asm"

            asm_file.write_text(f"{fasm_mode}\n{code}", encoding="utf-8")

            run_executable([FASM_EXECUTABLE_PATH, asm_file], stdout=DEVNULL, check=True)
            code = asm_file.with_suffix(".bin").read_bytes()

    if not isinstance(code, bytes):
        raise TypeError("code must be bytes | str")

    return code


def get_simple_jump_code(address: int, ip: int) -> str:
    return f"""
        jmp {address - ip}
    """


def get_long_x64_jump_to_new_mem_code(address: int) -> str:
    return f"""
        push rax
        mov rax, {address}
        push rax
        ret
        pop rax
    """


def get_long_x64_jump_back_code(address: int) -> str:
    return f"""
        mov rax, {address}
        push rax
        ret
    """


def safely_eject_all_code_injections() -> None:
    for injection in AbstractCodeInjection.created_code_injections:
        with suppress(MemoryWriteError):
            injection.eject()
