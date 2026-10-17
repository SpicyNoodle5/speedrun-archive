from tkinter import Canvas, Entry, Frame, Label

class TimeInput(Frame):
    _INPUT_WIDTH: int = 5

    def __init__(self, parent: Canvas | Frame):
        super().__init__(parent)
        minutes_separator: Label = Label(self, text=":")
        seconds_separator: Label = Label(self, text=":")
        millis_separator: Label = Label(self, text=".")
        self._hour_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._minute_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._second_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._millis_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._hour_input.grid(column=0, row=0)
        minutes_separator.grid(column=1, row=0)
        self._minute_input.grid(column=2, row=0)
        seconds_separator.grid(column=3, row=0)
        self._second_input.grid(column=4, row=0)
        millis_separator.grid(column=5, row=0)
        self._millis_input.grid(column=6, row=0)

    def get(self) -> str:
        hour: str = self._hour_input.get()
        minute: str = self._minute_input.get()
        second: str = self._second_input.get()
        millis: str = self._millis_input.get()

        return ':'.join([self._time_part(hour), self._time_part(minute), self._time_part(second)]) + '.' + self._time_part(millis, 3)

    def _time_part(self, part: str, length: int = 2) -> str:
        if not part:
            return "0" * length
        if len(part) < length:
            return "0" * (length - len(part)) + part
        return part

class DateInput(Frame):
    _INPUT_WIDTH: int = 5
    _PAD: int = 10

    def __init__(self, parent: Canvas):
        super().__init__(parent)
        year_label: Label = Label(self, text="Year")
        month_label: Label = Label(self, text="Month")
        day_label: Label = Label(self, text="Day")
        self._year_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._month_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        self._day_input: Entry = Entry(self, width=self._INPUT_WIDTH)
        year_label.grid(column=0, row=0)
        self._year_input.grid(column=1, row=0, padx=self._PAD)
        month_label.grid(column=2, row=0)
        self._month_input.grid(column=3, row=0, padx=self._PAD)
        day_label.grid(column=4, row=0)
        self._day_input.grid(column=5, row=0)

    def get(self) -> str:
        year: str = self._year_input.get()
        month: str = self._month_input.get()
        day: str = self._day_input.get()
        return '-'.join([year, self._calendar_part(month), self._calendar_part(day)])

    def _calendar_part(self, part: str) -> str:
        if not part:
            return "00"
        if len(part) < 2:
            return "0" * (2 - len(part)) + part
        return part
