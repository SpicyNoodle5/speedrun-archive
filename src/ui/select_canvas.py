from tkinter import Button, Canvas, Label, Tk
from collections.abc import Callable
import os

class SelectCanvas(Canvas):
    _PAD: int = 10

    def __init__(self, parent: Tk, archive_dir: str, on_click_submit: Callable[[str], None]) -> None:
        super().__init__(parent)
        self._create_ui(archive_dir, on_click_submit)

    def _read_games(self, archive_dir: str) -> list[str]:
        if not os.path.isdir(archive_dir):
            return []
        return [d for d in os.listdir(archive_dir) if os.path.isdir('/'.join([archive_dir, d]))]

    def _create_ui(self, archive_dir: str, on_click_submit: Callable[[str], None]) -> None:
        for i, game_dir in enumerate(self._read_games(archive_dir)):
            self._create_game_row(i, game_dir, on_click_submit)

    def _create_game_row(self, row: int, game_dir: str, on_click_submit: Callable[[str], None]) -> None:
        game_label: Label = Label(self, text=game_dir)
        submit_button: Button = Button(self, text="Submit Run", command=lambda: on_click_submit(game_dir))
        game_label.grid(column=0, row=row, padx=self._PAD, pady=self._PAD)
        submit_button.grid(column=2, row=row, padx=self._PAD)
