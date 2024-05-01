import asyncio
import locale

from aiogram import Bot
from loguru import logger

from pkg.logging import Logger
from src.bot.bot import TgBot
from src.lexicon.lexicon import Lexicon
from src.bot.routers.routers import routers
from src.config import Config
from src.storage.db.connect import DBConnect
from src.storage.redis.db_redis import RedisDatabase
from src.storage.storage import Storage


async def main() -> None:
    cfg = Config()

    log = Logger(
        log_level=cfg.log_level,
        log_dir_name=cfg.paths.log_dir_name,
        info_log_path=cfg.paths.info_log_path,
    )
    log.setup_logger()
    logger.info("setup logger")
    logger.debug("debug is ON")

    bot = Bot(token=cfg.bot.token)

    storage = Storage(
        db=DBConnect(cfg.db.build_connection_str),
        redis=RedisDatabase(cfg),
    )

    lexicon = Lexicon()

    tg_bot = TgBot(
        bot=bot,
        storage=storage,
        lexicon=lexicon,
    )
    tg_bot.set_routers(routers)
    tg_bot.set_cfg(cfg)

    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

    await asyncio.gather(
        tg_bot.run(
            lexicon=lexicon,
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
