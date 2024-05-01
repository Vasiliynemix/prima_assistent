import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class BotConfig:
    token: str = os.getenv("TG_BOT_TOKEN")


@dataclass
class DBConfig:
    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USERNAME")
    passwd: str = os.getenv("DB_PASSWORD")
    port: int = int(os.getenv("DB_PORT"))
    host: str = os.getenv("DB_HOST")

    driver: str = os.getenv("DRIVER")
    database_system: str = os.getenv("DATABASE_SYSTEM")

    @property
    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    db: int = int(os.getenv("REDIS_DATABASE", 1))
    host: str = os.getenv("REDIS_HOST", "redis")
    port: int = int(os.getenv("REDIS_PORT", 6379))
    passwd: str | None = os.getenv("REDIS_PASSWORD")
    username: str | None = os.getenv("REDIS_USERNAME")
    state_ttl: int | None = os.getenv("REDIS_TTL_STATE", None)
    data_ttl: int | None = os.getenv("REDIS_TTL_DATA", None)


@dataclass
class PathsConfig:
    root_path: str = str(Path(__file__).parent.parent)

    log_dir_name: str = os.getenv("LOG_DIR_NAME")
    _info_log_file_name: str = os.getenv("INFO_LOG_FILE_NAME")

    @property
    def info_log_path(self) -> str:
        return os.path.join(self.root_path, self.log_dir_name, self._info_log_file_name)


@dataclass
class VideoLinkConfig:
    about_ak_24: str = os.getenv("VIDEO_LINK_ABOUT_AK_24")
    about_guard: str = os.getenv("VIDEO_LINK_ABOUT_GUARD")
    about_helper: str = os.getenv("VIDEO_LINK_ABOUT_HELPER")
    about_site: str = os.getenv("VIDEO_LINK_ABOUT_SITE")


@dataclass
class BoostConfig:
    ak_24: str = os.getenv("AK_24")
    guard: str = os.getenv("GUARD")
    helper: str = os.getenv("HELPER")
    site: str = os.getenv("SITE")
    boosts: tuple[str] = (ak_24, guard, helper, site)


@dataclass
class Config:
    log_level: str = os.getenv("LOG_LEVEL")
    chat_link: str = os.getenv("CHAT_LINK")
    site_link: str = os.getenv("SITE_LINK")

    time_format = os.getenv("TIME_FORMAT")
    admins: list[int] = field(
        default_factory=lambda: list(map(int, os.getenv("ADMINS").split(",")))
    )

    bot: BotConfig = field(default_factory=BotConfig)
    db: DBConfig = field(default_factory=DBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    boost: BoostConfig = field(default_factory=BoostConfig)
    video_link: VideoLinkConfig = field(default_factory=VideoLinkConfig)


cfg = Config()
