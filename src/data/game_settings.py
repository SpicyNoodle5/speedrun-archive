from dataclasses import asdict, dataclass, field
from data.leaderboard import Leaderboard
import os
import json

SETTINGS_PATH: str = "settings.json"

@dataclass
class Subcategory:
    """
    Represents a subcategory, these are stored in the archive as key, value lists.
    e.g "Version: 1.0"
    """
    name: str
    values: list[str] = field(default_factory=list)

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
    subcategories: list[dict] = field(default_factory=list)

    @staticmethod
    def read(dir: str):
        if not os.path.isdir(dir):
            return None
        if not os.path.isfile(GameSettings._file_path(dir)):
            return GameSettings._read_from_leaderboard(dir)
        with open(GameSettings._file_path(dir), 'r') as f:
            settings = GameSettings(**json.loads(f.read()))
        instantiated_subcategories: list[Subcategory] = []
        for subcategory in settings.subcategories:
            if type(subcategory) is Subcategory:
                instantiated_subcategories.append(subcategory)
            else:
                instantiated_subcategories.append(Subcategory(subcategory["name"], subcategory["values"]))
        settings.subcategories = instantiated_subcategories
        return settings

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
            if row[leaderboard.SUBCATEGORIES]:
                found_subcategories = row[leaderboard.SUBCATEGORIES].split(", ")
                for found_subcategory in found_subcategories:
                    if found_subcategory not in subcategories:
                        subcategories.append(found_subcategory)
        if Leaderboard.REALTIME_NO_LOADS in leaderboard.data[0].keys():
            game_settings.use_lrt = True
        subcategory_by_name: dict[str, Subcategory] = {}
        for subcategory in subcategories:
            subcategory_parts: list[str] = subcategory.split(": ")
            if len(subcategory_parts) == 2:
                name: str = subcategory_parts[0]
                value: str = subcategory_parts[1]
                if name in subcategory_by_name.keys():
                    subcategory_by_name[name].values.append(value)
                else:
                    subcategory_by_name[name] = Subcategory(name, [value])
        game_settings.subcategories = [*subcategory_by_name.values()]
        game_settings.write(dir)
        return game_settings

    def sort(self) -> None:
        self.levels.sort()
        self.full_game_categories.sort()
        self.level_categories.sort()
        self.regions.sort()
        self.platforms.sort()
        for subcategory in self.subcategories:
            subcategory.values.sort()

    def write(self, dir: str) -> None:
        if not os.path.isdir(dir):
            return
        with open(GameSettings._file_path(dir), 'w') as f:
            json.dump(asdict(self), f, indent=4)

    @staticmethod
    def _file_path(dir: str) -> str:
        return '/'.join([dir, SETTINGS_PATH])
