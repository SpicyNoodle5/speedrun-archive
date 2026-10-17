from dataclasses import dataclass
from data.game_settings import GameSettings
from data.leaderboard import Leaderboard
from datetime import datetime, timezone
import re

class SubmissionRegex:
    TIME_REGEX: str = r"\d{2}:\d{2}:\d{2}\.\d{3}"
    DATE_REGEX: str = r"\d{4}-\d{2}-\d{2}"
    SRC_URL_REGEX: str = r".*/www\.speedrun\.com/\w+/runs/\w+"

@dataclass
class SubmissionData:
    verification_status: str
    category: str
    level: str | None
    subcategories: str
    player: str
    real_time: str
    load_removed_time: str | None
    date: str
    platform: str
    emulated: bool
    region: str
    video_url: str
    description: str
    src_url: str

    def validate(self, is_full_game: bool, settings: GameSettings) -> bool:
        if not self.verification_status:
            return False
        if is_full_game and self.level:
            return False
        if not is_full_game and self.level not in settings.levels:
            return False
        if is_full_game and self.category not in settings.full_game_categories:
            return False
        if not is_full_game and self.category not in settings.level_categories:
            return False
        if not self.player:
            return False
        if not re.match(SubmissionRegex.TIME_REGEX, self.real_time):
            return False
        if settings.use_lrt and is_full_game:
            if not self.load_removed_time or not re.match(SubmissionRegex.TIME_REGEX, self.load_removed_time):
                return False
        else:
            if self.load_removed_time:
                return False
        if not re.match(SubmissionRegex.DATE_REGEX, self.date):
            return False
        if self.platform not in settings.platforms:
            return False
        if self.region not in settings.regions:
            return False
        if not self.video_url:
            return False
        if not self.src_url or not re.match(SubmissionRegex.SRC_URL_REGEX, self.src_url):
            return False
        
        return True

    def to_dict(self, settings: GameSettings) -> dict:
        # Assume primary time is real time, not LRT
        # This will need changing if any games that rank by LRT want to use this tool
        primary_time: str = self.real_time
        primary_time_parts: list[str] = primary_time.split(':')
        primary_seconds: float = int(primary_time_parts[0]) * 60 * 60 + int(primary_time_parts[1]) * 60 + float(primary_time_parts[2])

        src_run_id: str = self.src_url.split('/')[-1]
        submitted_timestamp: str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        data = {
            Leaderboard.STATUS: self.verification_status,
            Leaderboard.CATEGORY: self.category,
            Leaderboard.LEVEL: self.level,
            Leaderboard.SUBCATEGORIES: self.subcategories,
            Leaderboard.PLAYERS: self.player,
            Leaderboard.PRIMARY_TIME: primary_time,
            Leaderboard.PRIMARY_SECONDS: int(primary_seconds) if primary_seconds.is_integer() else primary_seconds,
            Leaderboard.REALTIME: self.real_time,
            Leaderboard.DATE: self.date,
            Leaderboard.PLATFORM: self.platform,
            Leaderboard.EMULATED: "TRUE" if self.emulated else "FALSE",
            Leaderboard.REGION: self.region,
            Leaderboard.VIDEO: self.video_url,
            Leaderboard.COMMENT: self.description,
            Leaderboard.SRC_RUN_ID: src_run_id,
            Leaderboard.SUBMITTED_DATETIME: submitted_timestamp
        }

        if settings.use_lrt:
            data[Leaderboard.REALTIME_NO_LOADS] = self.load_removed_time
        return data
