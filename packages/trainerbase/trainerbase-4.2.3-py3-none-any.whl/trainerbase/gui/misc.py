from collections.abc import Callable
from typing import override

from dearpygui import dearpygui as dpg

from trainerbase.common.keyboard import (
    AbstractKeyboardHandler,
    ReleaseHotkeySwitch,
    ShortLongHotkeyPressSwitch,
    SimpleHotkeyHandler,
)
from trainerbase.gui.types import AbstractUIComponent


class SeparatorUI(AbstractUIComponent):
    def __init__(self, empty_lines_before: int = 1, empty_lines_after: int = 0):
        self._empty_lines_before = empty_lines_before
        self._empty_lines_after = empty_lines_after

    @override
    def add_to_ui(self) -> None:
        for _ in range(self._empty_lines_before):
            dpg.add_text()

        dpg.add_separator()

        for _ in range(self._empty_lines_after):
            dpg.add_text()


class TextUI(AbstractUIComponent):
    def __init__(self, text: str = ""):
        self.text = text

    @override
    def add_to_ui(self) -> None:
        dpg.add_text(self.text)


class HotkeyHandlerUI(AbstractUIComponent):
    def __init__(
        self,
        handler: AbstractKeyboardHandler,
        label: str,
    ):
        self.handler = handler
        self.label = label

    @override
    def add_to_ui(self) -> None:
        match self.handler:
            case ShortLongHotkeyPressSwitch():
                dpg.add_text(f"Hold [{self.handler.hotkey}] Enable {self.label}")
                dpg.add_text(f"Press [{self.handler.hotkey}] Toggle {self.label}")
            case ReleaseHotkeySwitch():
                dpg.add_text(f"[{self.handler.hotkey}] Toggle {self.label}")
            case SimpleHotkeyHandler():
                dpg.add_button(
                    label=f"[{self.handler.hotkey}] {self.label}",
                    callback=self._ensure_callable_has_dunder_code(self.handler.callback),
                )
            case _:
                dpg.add_text(f"[{self.handler.hotkey}] {self.label}")

        self.handler.handle()

    @staticmethod
    def _ensure_callable_has_dunder_code(callable_object: Callable[[], None]) -> Callable[[], None]:
        """
        DPG add_button has `callback` arg. In this case `callback.__code__` is required.
        """

        if hasattr(callable, "__code__"):
            callback_with_dunder_code = callable_object
        else:

            def callback_with_dunder_code():
                callable_object()

        return callback_with_dunder_code
