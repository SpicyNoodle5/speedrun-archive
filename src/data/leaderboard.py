import csv

class Leaderboard:
    STATUS: str = "Status"
    CATEGORY: str = "Category"
    LEVEL: str = "Level"
    SUBCATEGORIES: str = "Subcategories"
    PLAYERS: str = "Players"
    PRIMARY_TIME: str = "Primary Time"
    PRIMARY_SECONDS: str = "Primary Seconds"
    REALTIME: str = "Realtime"
    REALTIME_NO_LOADS: str = "Realtime No Loads"
    DATE: str = "Date"
    PLATFORM: str = "Platform"
    EMULATED: str = "Emulated"
    REGION: str = "Region"
    VIDEO: str = "Video"
    COMMENT: str = "Comment"
    SRC_RUN_ID: str = "Run ID"
    SUBMITTED_DATETIME: str = "Submitted"

    _LEADERBOARD_PATH: str = "leaderboard.csv"
    _ENCODING: str = "utf-8"

    def __init__(self, dir: str) -> None:
        self.data: dict = None
        self.dir: str = dir
        self._read()

    def _read(self) -> None:
        with open(self._file_path(), 'r', encoding=self._ENCODING) as f:
            self.data = list(csv.DictReader(f))

    def add_run(self, data: dict) -> None:
        with open(self._file_path(), 'a', encoding=self._ENCODING, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)
 
    def _file_path(self) -> str:
        return '/'.join([self.dir, self._LEADERBOARD_PATH])
