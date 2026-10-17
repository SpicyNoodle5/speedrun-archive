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

    def __init__(self, dir: str) -> None:
        self.data: dict = None
        self._read(dir)

    def _read(self, dir: str) -> None:
        with open('/'.join([dir, self._LEADERBOARD_PATH]), 'r', encoding="utf-8") as f:
            self.data = list(csv.DictReader(f))

    def add_run(self, dir: str, data: dict) -> None:
        pass
