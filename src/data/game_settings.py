from dataclasses import asdict, dataclass, field
from data.leaderboard import Leaderboard
import os
import json

@dataclass
class Subcategory:
    """
    Represents a subcategory, these are stored in the archive as key, value pairs.
    e.g "Version: 1.0"
    """
    name: str
    value: str

@dataclass
class GameSettings:
    """
    Represents the game's leaderboard settings
    """
    full_game_categories: list[str] = field(default_factory=list)
    level_categories: list[str] = field(default_factory=list)
    levels: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    use_lrt: bool = field(default=False)
    subcategories: list = field(default_factory=list)

    _SETTINGS_PATH: str = "settings.json"

    @staticmethod
    def read(dir: str):
        if not os.path.isdir(dir):
            return None
        if not os.path.isfile(GameSettings._file_path(dir)):
            return GameSettings._read_from_leaderboard(dir)
        with open(GameSettings._file_path(dir), 'r') as f:
            return GameSettings(**json.loads(f.read()))

    @staticmethod
    def _read_from_leaderboard(dir: str):
        leaderboard: Leaderboard = Leaderboard(dir)
        if leaderboard.data is None or len(leaderboard.data) == 0:
            return None
        game_settings: GameSettings = GameSettings()
        subcategories: list[str] = []
        for row in leaderboard.data:
            if Leaderboard.LEVEL in leaderboard.data[0].keys():
                if row[leaderboard.CATEGORY] not in game_settings.full_game_categories and not row[leaderboard.LEVEL]:
                    game_settings.full_game_categories.append(row[leaderboard.CATEGORY])
                if row[leaderboard.CATEGORY] not in game_settings.level_categories and row[leaderboard.LEVEL]:
                    game_settings.level_categories.append(row[leaderboard.CATEGORY])
                if row[leaderboard.LEVEL] and row[leaderboard.LEVEL] not in game_settings.levels:
                    game_settings.levels.append(row[leaderboard.LEVEL])
            else:
                if row[leaderboard.CATEGORY] not in game_settings.full_game_categories:
                    game_settings.full_game_categories.append(row[leaderboard.CATEGORY])
            if row[leaderboard.PLATFORM] and row[leaderboard.PLATFORM] not in game_settings.platforms:
                game_settings.platforms.append(row[leaderboard.PLATFORM])
            if row[leaderboard.REGION] and row[leaderboard.REGION] not in game_settings.regions:
                game_settings.regions.append(row[leaderboard.REGION])
            if row[leaderboard.SUBCATEGORIES] and row[leaderboard.SUBCATEGORIES] not in subcategories:
                subcategories.append(row[leaderboard.SUBCATEGORIES])
        if Leaderboard.REALTIME_NO_LOADS in leaderboard.data[0].keys():
            game_settings.use_lrt = True
        for subcategory in subcategories:
            subcategory_parts: list[str] = subcategory.split(": ")
            if len(subcategory_parts) == 2:
                game_settings.subcategories.append(Subcategory(subcategory_parts[0], subcategory_parts[1]))
        game_settings.write(dir)
        return game_settings

    def write(self, dir: str) -> None:
        if not os.path.isdir(dir):
            return
        with open(GameSettings._file_path(dir), 'w') as f:
            json.dump(asdict(self), f, indent=4)

    @staticmethod
    def _file_path(dir: str) -> str:
        return '/'.join([dir, GameSettings._SETTINGS_PATH])
