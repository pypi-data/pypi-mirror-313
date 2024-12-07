from typing import override

from dearpygui import dearpygui as dpg

from trainerbase.common.keyboard import ShortLongHotkeyPressSwitch, Switchable
from trainerbase.gui.helpers import add_components
from trainerbase.gui.misc import HotkeyHandlerUI
from trainerbase.gui.types import AbstractUIComponent
from trainerbase.speedhack import SpeedHack


class SpeedHackUISwitch(Switchable):
    def __init__(self, speedhack: SpeedHack, dpg_tag: str):
        self.speedhack = speedhack
        self.dpg_tag = dpg_tag

    @override
    def enable(self):
        self.speedhack.factor = dpg.get_value(self.dpg_tag)

    @override
    def disable(self):
        self.speedhack.factor = 1.0


class SpeedHackUI(AbstractUIComponent):
    DPG_TAG_SPEEDHACK_FACTOR_INPUT = "tag_speedhack_factor_input"
    DPG_TAG_SPEEDHACK_PRESET_INPUT = "tag_speedhack_preset_input"

    PRESETS: tuple[float, ...] = (0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0)

    def __init__(
        self,
        speedhack: SpeedHack | None = None,
        key: str = "Delete",
        default_factor_input_value: float = 3.0,
    ):
        self.speedhack = SpeedHack() if speedhack is None else speedhack
        self.key = key
        self.default_factor_input_value = default_factor_input_value
        self.handler = ShortLongHotkeyPressSwitch(
            SpeedHackUISwitch(self.speedhack, self.DPG_TAG_SPEEDHACK_FACTOR_INPUT),
            key,
        )

    @override
    def add_to_ui(self) -> None:
        add_components(HotkeyHandlerUI(self.handler, "SpeedHack"))

        dpg.add_input_double(
            tag=self.DPG_TAG_SPEEDHACK_FACTOR_INPUT,
            label="SpeedHack Factor",
            min_value=0.0,
            max_value=100.0,
            default_value=self.default_factor_input_value,
            min_clamped=True,
            max_clamped=True,
            callback=self.on_factor_change,
        )

        dpg.add_slider_int(
            tag=self.DPG_TAG_SPEEDHACK_PRESET_INPUT,
            label="Preset",
            min_value=0,
            max_value=len(self.PRESETS) - 1,
            clamped=True,
            default_value=self.get_closest_preset_index(self.default_factor_input_value),
            callback=self.on_preset_change,
        )

    def on_preset_change(self):
        new_factor = self.PRESETS[dpg.get_value(self.DPG_TAG_SPEEDHACK_PRESET_INPUT)]
        dpg.set_value(self.DPG_TAG_SPEEDHACK_FACTOR_INPUT, new_factor)

    def on_factor_change(self):
        new_factor = dpg.get_value(self.DPG_TAG_SPEEDHACK_FACTOR_INPUT)
        closest_preset_index = self.get_closest_preset_index(new_factor)
        dpg.set_value(self.DPG_TAG_SPEEDHACK_PRESET_INPUT, closest_preset_index)

    def get_closest_preset_index(self, factor: float) -> int:
        closest_preset = min(self.PRESETS, key=lambda preset: abs(preset - factor))
        return self.PRESETS.index(closest_preset)
