from tkinter import BooleanVar, Canvas, Checkbutton, Frame, Label 
from tkinter.ttk import Combobox
from data.game_settings import GameSettings, Subcategory

class SubcategoryFrame(Frame):
    def __init__(self, parent: Canvas, settings: GameSettings) -> None:
        super().__init__(parent)
        self._subcategory_inputs: list[SubcategoryInput] = []
        for subcategory in settings.subcategories:
            subcategory_input: SubcategoryInput = SubcategoryInput(self, subcategory)
            self._subcategory_inputs.append(subcategory_input)
            subcategory_input.pack()

    def get(self) -> str:
        entries: list[str] = [subcategory_input.get() for subcategory_input in self._subcategory_inputs]
        return ", ".join(filter(None, entries))

class SubcategoryInput(Frame):
    def __init__(self, parent: SubcategoryFrame, subcategory: Subcategory) -> None:
        super().__init__(parent)
        self._subcategory = subcategory
        label: Label = Label(self, text=subcategory.name)
        self._value_select: Combobox = Combobox(self, values=subcategory.values)
        self._is_enabled = BooleanVar(self, False)
        enabled_checkbox: Checkbutton = Checkbutton(self, text="Enabled", variable=self._is_enabled)
        label.grid(column=0, row=0)
        self._value_select.grid(column=1, row=0)
        enabled_checkbox.grid(column=2, row=0)

    def get(self) -> str | None:
        if not self._is_enabled.get():
            return None
        return ": ".join([self._subcategory.name, self._value_select.get()])
