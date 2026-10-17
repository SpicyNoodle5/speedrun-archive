from tkinter import Canvas, Tk
from ui.select_canvas import SelectCanvas
from ui.submit_canvas import SubmitCanvas

class Main:
    _ARCHIVE_DIR: str = "archive"
    _WINDOW_WIDTH: int = 800
    _WINDOW_HEIGHT: int = 600

    def __init__(self) -> None:
        self._window = Tk()
        self._window.title("Speedrun Archive Tool")
        self._window.geometry('x'.join([str(self._WINDOW_WIDTH), str(self._WINDOW_HEIGHT)]))
        self._select_canvas: SelectCanvas = SelectCanvas(self._window, self._ARCHIVE_DIR, self.open_submit)
        self._submit_canvas: SubmitCanvas = SubmitCanvas(self._window, self._ARCHIVE_DIR)
        self._current_canvas: Canvas = None
        self.open_select()

    def open_select(self) -> None:
        self._change_canvas(self._select_canvas)

    def open_submit(self, game: str) -> None:
        self._change_canvas(self._submit_canvas)
        self._submit_canvas.set_game(game)

    def _change_canvas(self, canvas: Canvas) -> None:
        if self._current_canvas is not None:
            self._current_canvas.pack_forget()
        self._current_canvas = canvas
        self._current_canvas.pack()

    def main(self) -> None:
        self._window.mainloop()

if __name__ == "__main__":
    main: Main = Main()
    main.main()
