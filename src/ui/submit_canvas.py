from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, Frame, Label, Radiobutton, StringVar, Text, Tk
from tkinter.ttk import Combobox
from data.game_settings import GameSettings
from data.leaderboard import Leaderboard

class SubmitCanvas(Canvas):
    _PAD: int = 10
    _TIME_INPUT_WIDTH: int = 5
    _DESCRIPTION_WIDTH: int = 30
    _DESCRIPTION_HEIGHT: int = 5

    def __init__(self, parent: Tk, archive_dir: str) -> None:
        super().__init__(parent)
        self._archive_dir: str = archive_dir
        self._current_settings: GameSettings = None
        self._current_leaderboard: Leaderboard = None
        self._full_game_submit_canvas: Canvas = Canvas(self)
        self._level_submit_canvas: Canvas = Canvas(self)
        self._common_canvas: Canvas = Canvas(self)
        self._show_full_game: BooleanVar = BooleanVar(self, True)
        self._verified_status = StringVar(parent, "verified")
        self._lrt_frame: Frame = None
        self._lrt_row: int = 0

    def set_game(self, game: str) -> None:
        self._current_settings = GameSettings.read(self._game_dir(game))
        self._current_leaderboard = Leaderboard(self._game_dir(game))
        self._create_ui(game)

    def _create_ui(self, game: str):
        self._create_ui_full_game()
        self._create_ui_level()
        # Header widgets
        header_canvas: Canvas = Canvas(self)
        game_label: Label = Label(header_canvas, text=game)
        full_game_run_button: Radiobutton = Radiobutton(header_canvas, text="Submit Full Game Run", indicatoron=0, variable=self._show_full_game, value=True, command=lambda: self._toggle_submit_mode())
        level_run_button: Radiobutton = Radiobutton(header_canvas, text="Submit Level Run", indicatoron=0, variable=self._show_full_game, value=False, command=lambda: self._toggle_submit_mode())
        game_label.grid(column=0, row=0, columnspan=2, pady=self._PAD)
        full_game_run_button.grid(column=0, row=1, padx=self._PAD, pady=self._PAD)
        level_run_button.grid(column=1, row=1, padx=self._PAD)
        # LRT on its own frame so it can be hidden
        self._lrt_frame = Frame(self._common_canvas)
        lrt_label: Label = Label(self._lrt_frame, text="Load Removed Time")
        lrt_input: Frame = self._create_time_input(self._lrt_frame)
        lrt_label.grid(column=0, row=0, columnspan=2, padx=self._PAD, pady=self._PAD)
        lrt_input.grid(column=2, row=0, columnspan=2, padx=self._PAD)
        # Common submit widgets between full game and level runs
        real_time_frame: Frame = Frame(self._common_canvas)
        real_time_label: Label = Label(real_time_frame, text="Real Time")
        real_time_input: Frame = self._create_time_input(real_time_frame)
        real_time_label.grid(column=0, row=0, columnspan=2, padx=self._PAD, pady=self._PAD)
        real_time_input.grid(column=2, row=0, columnspan=2, padx=self._PAD)
        date_label: Label = Label(self._common_canvas, text="Date Performed")
        date_input: Frame = self._create_date_input(self._common_canvas)
        video_label: Label = Label(self._common_canvas, text="Video URL")
        video_input: Entry = Entry(self._common_canvas)
        src_label: Label = Label(self._common_canvas, text="Speedrun.com URL")
        src_input: Label = Entry(self._common_canvas)
        player_label: Label = Label(self._common_canvas, text="Player")
        player_input: Entry = Entry(self._common_canvas)
        region_label: Label = Label(self._common_canvas, text="Region")
        region_select: Combobox = Combobox(self._common_canvas, values=self._current_settings.regions)
        platform_label: Label = Label(self._common_canvas, text="Platform")
        platform_select: Combobox = Combobox(self._common_canvas, values=self._current_settings.platforms)
        emulator_label: Label = Label(self._common_canvas, text="Emulator")
        emulator_checkbox: Checkbutton = Checkbutton(self._common_canvas)
        description_label: Label = Label(self._common_canvas, text="Description")
        description_input: Label = Text(self._common_canvas, width=self._DESCRIPTION_WIDTH, height=self._DESCRIPTION_HEIGHT)
        status_label: Label = Label(self._common_canvas, text="Verification Status")
        verified_button: Radiobutton = Radiobutton(self._common_canvas, text="Verified", variable=self._verified_status, value="verified")
        rejected_button: Radiobutton = Radiobutton(self._common_canvas, text="Rejected", variable=self._verified_status, value="rejected")
        submit_button: Button = Button(self._common_canvas, text="Submit", command=lambda: self._submit())
        current_row: int = 0
        real_time_frame.grid(column=0, row=current_row, columnspan=4)
        current_row += 1
        self._lrt_row = current_row
        self._toggle_lrt()
        current_row += 1
        date_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        date_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        video_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        video_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        src_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD)
        src_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        player_label.grid(column=0, row=current_row, padx=self._PAD, pady=self._PAD)
        player_input.grid(column=1, row=current_row, padx=self._PAD)
        region_label.grid(column=2, row=current_row, padx=self._PAD)
        region_select.grid(column=3, row=current_row, padx=self._PAD)
        current_row += 1
        platform_label.grid(column=0, row=current_row, padx=self._PAD, pady=self._PAD)
        platform_select.grid(column=1, row=current_row, padx=self._PAD)
        emulator_label.grid(column=2, row=current_row, padx=self._PAD)
        emulator_checkbox.grid(column=3, row=current_row, padx=self._PAD)
        current_row += 1
        description_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        description_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        status_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        verified_button.grid(column=2, row=current_row, padx=self._PAD)
        rejected_button.grid(column=3, row=current_row, padx=self._PAD)
        current_row += 1
        submit_button.grid(column=1, row=current_row, columnspan=2, pady=self._PAD)
        header_canvas.pack()
        self._full_game_submit_canvas.pack()
        self._common_canvas.pack()
        
    def _create_ui_full_game(self) -> None:
        category_label: Label = Label(self._full_game_submit_canvas, text="Category")
        category_select: Combobox = Combobox(self._full_game_submit_canvas, values=self._current_settings.full_game_categories)
        category_label.grid(column=0, row=0, padx=self._PAD, pady=self._PAD)
        category_select.grid(column=1, row=0, padx=self._PAD)

    def _create_ui_level(self) -> None:
        category_label: Label = Label(self._level_submit_canvas, text="Category")
        category_select: Combobox = Combobox(self._level_submit_canvas, values=self._current_settings.level_categories)
        level_label: Label = Label(self._level_submit_canvas, text="Level")
        level_select: Combobox = Combobox(self._level_submit_canvas, values=self._current_settings.levels)
        category_label.grid(column=0, row=0, padx=self._PAD, pady=self._PAD)
        category_select.grid(column=1, row=0, padx=self._PAD)
        level_label.grid(column=2, row=0, padx=self._PAD)
        level_select.grid(column=3, row=0, padx=self._PAD)

    def _create_time_input(self, parent: Frame) -> Frame:
        frame: Frame = Frame(parent)
        minutes_separator: Label = Label(frame, text=":")
        seconds_separator: Label = Label(frame, text=":")
        millis_separator: Label = Label(frame, text=".")
        hour_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        minute_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        second_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        millis_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        hour_input.grid(column=0, row=0)
        minutes_separator.grid(column=1, row=0)
        minute_input.grid(column=2, row=0)
        seconds_separator.grid(column=3, row=0)
        second_input.grid(column=4, row=0)
        millis_separator.grid(column=5, row=0)
        millis_input.grid(column=6, row=0)
        return frame

    def _create_date_input(self, parent: Canvas) -> Frame:
        frame: Frame = Frame(parent)
        year_label: Label = Label(frame, text="Year")
        month_label: Label = Label(frame, text="Month")
        day_label: Label = Label(frame, text="Day")
        year_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        month_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        day_input: Entry = Entry(frame, width=self._TIME_INPUT_WIDTH)
        year_label.grid(column=0, row=0)
        year_input.grid(column=1, row=0, padx=self._PAD)
        month_label.grid(column=2, row=0)
        month_input.grid(column=3, row=0, padx=self._PAD)
        day_label.grid(column=4, row=0)
        day_input.grid(column=5, row=0)
        return frame

    def _toggle_submit_mode(self) -> None:
        self._common_canvas.pack_forget()
        if self._show_full_game.get():
            self._level_submit_canvas.pack_forget()
            self._full_game_submit_canvas.pack()
        else:
            self._full_game_submit_canvas.pack_forget()
            self._level_submit_canvas.pack()
        self._common_canvas.pack()
        self._toggle_lrt()

    def _toggle_lrt(self) -> None:
        if self._show_full_game.get() and self._current_settings.use_lrt:
            self._lrt_frame.grid(column=0, row=self._lrt_row, columnspan=4)
        else:
            self._lrt_frame.grid_forget()

    def _submit(self) -> None:
        pass

    def _game_dir(self, game: str) -> str:
        return '/'.join([self._archive_dir, game])
