from tkinter import BooleanVar, Button, Canvas, Checkbutton, Entry, Frame, Label, Radiobutton, StringVar, Text, Tk
from tkinter.ttk import Combobox
from data.game_settings import GameSettings
from data.leaderboard import Leaderboard
from data.submission import SubmissionData
from ui.subcategory_input import SubcategoryFrame
from ui.time_input import DateInput, TimeInput

class SubmitCanvas(Canvas):
    _PAD: int = 10
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
        self._status_canvas: Canvas = Canvas(self)
        self._show_full_game: BooleanVar = BooleanVar(self, True)
        self._verified_status = StringVar(parent, "verified")
        self._use_emulator: BooleanVar = BooleanVar(self, False)
        self._lrt_frame: Frame = None
        self._lrt_row: int = 0
        self._full_game_category_select: Combobox = None
        self._level_category_select: Combobox = None
        self._level_select: Combobox = None
        self._subcategory_frame: SubcategoryFrame = None
        self._real_time_input: TimeInput = None
        self._lrt_input: TimeInput = None
        self._date_input: DateInput = None
        self._video_input: Entry = None
        self._src_input: Entry = None
        self._player_input: Entry = None
        self._region_select: Combobox = None
        self._platform_select: Combobox = None
        self._description_input: Text = None
        self._status_label: Label = None

    def set_game(self, game: str) -> None:
        self._current_settings = GameSettings.read(self._game_dir(game))
        self._current_leaderboard = Leaderboard(self._game_dir(game))
        self._current_settings.sort()
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
        self._lrt_input: TimeInput = TimeInput(self._lrt_frame)
        lrt_label.grid(column=0, row=0, columnspan=2, padx=self._PAD, pady=self._PAD)
        self._lrt_input.grid(column=2, row=0, columnspan=2, padx=self._PAD)
        # Common submit widgets between full game and level runs
        self._subcategory_frame: SubcategoryFrame = SubcategoryFrame(self._common_canvas, self._current_settings)
        real_time_frame: Frame = Frame(self._common_canvas)
        real_time_label: Label = Label(real_time_frame, text="Real Time")
        self._real_time_input: TimeInput = TimeInput(real_time_frame)
        real_time_label.grid(column=0, row=0, columnspan=2, padx=self._PAD, pady=self._PAD)
        self._real_time_input.grid(column=2, row=0, columnspan=2, padx=self._PAD)
        date_label: Label = Label(self._common_canvas, text="Date Performed")
        self._date_input: DateInput = DateInput(self._common_canvas)
        video_label: Label = Label(self._common_canvas, text="Video URL")
        self._video_input: Entry = Entry(self._common_canvas)
        src_label: Label = Label(self._common_canvas, text="Speedrun.com URL")
        self._src_input: Entry = Entry(self._common_canvas)
        player_label: Label = Label(self._common_canvas, text="Player")
        self._player_input: Entry = Entry(self._common_canvas)
        region_label: Label = Label(self._common_canvas, text="Region")
        self._region_select: Combobox = Combobox(self._common_canvas, values=self._current_settings.regions)
        platform_label: Label = Label(self._common_canvas, text="Platform")
        self._platform_select: Combobox = Combobox(self._common_canvas, values=self._current_settings.platforms)
        emulator_label: Label = Label(self._common_canvas, text="Emulator")
        emulator_checkbox: Checkbutton = Checkbutton(self._common_canvas, variable=self._use_emulator)
        description_label: Label = Label(self._common_canvas, text="Description")
        self._description_input: Text = Text(self._common_canvas, width=self._DESCRIPTION_WIDTH, height=self._DESCRIPTION_HEIGHT)
        status_label: Label = Label(self._common_canvas, text="Verification Status")
        verified_button: Radiobutton = Radiobutton(self._common_canvas, text="Verified", variable=self._verified_status, value="verified")
        rejected_button: Radiobutton = Radiobutton(self._common_canvas, text="Rejected", variable=self._verified_status, value="rejected")
        submit_button: Button = Button(self._common_canvas, text="Submit", command=lambda: self._submit())
        # Place widgets
        current_row: int = 0
        self._subcategory_frame.grid(column=0, row=current_row, columnspan=4)
        current_row += 1
        real_time_frame.grid(column=0, row=current_row, columnspan=4)
        current_row += 1
        self._lrt_row = current_row
        self._toggle_lrt()
        current_row += 1
        date_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        self._date_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        video_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        self._video_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        src_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD)
        self._src_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
        current_row += 1
        player_label.grid(column=0, row=current_row, padx=self._PAD, pady=self._PAD)
        self._player_input.grid(column=1, row=current_row, padx=self._PAD)
        region_label.grid(column=2, row=current_row, padx=self._PAD)
        self._region_select.grid(column=3, row=current_row, padx=self._PAD)
        current_row += 1
        platform_label.grid(column=0, row=current_row, padx=self._PAD, pady=self._PAD)
        self._platform_select.grid(column=1, row=current_row, padx=self._PAD)
        emulator_label.grid(column=2, row=current_row, padx=self._PAD)
        emulator_checkbox.grid(column=3, row=current_row, padx=self._PAD)
        current_row += 1
        description_label.grid(column=0, row=current_row, columnspan=2, padx=self._PAD, pady=self._PAD)
        self._description_input.grid(column=2, row=current_row, columnspan=2, padx=self._PAD)
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
        self._full_game_category_select: Combobox = Combobox(self._full_game_submit_canvas, values=self._current_settings.full_game_categories)
        category_label.grid(column=0, row=0, padx=self._PAD, pady=self._PAD)
        self._full_game_category_select.grid(column=1, row=0, padx=self._PAD)

    def _create_ui_level(self) -> None:
        category_label: Label = Label(self._level_submit_canvas, text="Category")
        self._level_category_select: Combobox = Combobox(self._level_submit_canvas, values=self._current_settings.level_categories)
        level_label: Label = Label(self._level_submit_canvas, text="Level")
        self._level_select: Combobox = Combobox(self._level_submit_canvas, values=self._current_settings.levels)
        category_label.grid(column=0, row=0, padx=self._PAD, pady=self._PAD)
        self._level_category_select.grid(column=1, row=0, padx=self._PAD)
        level_label.grid(column=2, row=0, padx=self._PAD)
        self._level_select.grid(column=3, row=0, padx=self._PAD)

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
        submission_data: SubmissionData = SubmissionData(
            self._verified_status.get(),
            self._full_game_category_select.get() if self._show_full_game.get() else self._level_category_select.get(),
            self._level_select.get() if not self._show_full_game.get() else None,
            self._subcategory_frame.get(),
            self._player_input.get(),
            self._real_time_input.get(),
            self._lrt_input.get() if self._current_settings.use_lrt and self._show_full_game.get() else None,
            self._date_input.get(),
            self._platform_select.get(),
            self._use_emulator.get(),
            self._region_select.get(),
            self._video_input.get(),
            self._description_input.get("1.0", "end-1c"),
            self._src_input.get()
        )
        if self._status_label is not None:
            self._status_label.pack_forget()
        if submission_data.validate(self._show_full_game.get(), self._current_settings):
            self._current_leaderboard.add_run(submission_data.to_dict(self._current_settings))
            self._status_label = Label(self._status_canvas, text="Run submitted!")
        else:
            self._status_label = Label(self._status_canvas, text="Run data invalid! Please check your input and submit again.")
        self._status_label.pack()
        self._status_canvas.pack()

    def _game_dir(self, game: str) -> str:
        return '/'.join([self._archive_dir, game])
