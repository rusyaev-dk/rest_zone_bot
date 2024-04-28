import asyncio
import logging
import os
from pathlib import Path

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from sqlalchemy.ext.asyncio import async_sessionmaker

from data.infrastructure.database.setup import create_engine, create_session_pool
from data.l10n.translator import TranslatorHub

from tgbot.config import load_config
from tgbot.handlers import routers_list
from tgbot.middlewares.database import OuterDatabaseMiddleware, InnerDatabaseMiddleware, UserExistingMiddleware
from tgbot.middlewares.l10n import L10nMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.constants import DEFAULT_THROTTLE_TIME
from tgbot.services import broadcaster


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


def setup_translator(
    locales_dir_path: str
) -> TranslatorHub:

    all_files = os.listdir(locales_dir_path + "/ru")
    fluent_files = [file for file in all_files if file.endswith(".ftl")]

    translator_hub = TranslatorHub(
        locales_dir_path=str(locales_dir_path), locales=["ru", "uz"],
        resource_ids=fluent_files
    )
    return translator_hub


def register_global_middlewares(
        dp: Dispatcher,
        translator_hub: TranslatorHub,
        session_pool: async_sessionmaker,
):
    dp.message.outer_middleware(OuterDatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(OuterDatabaseMiddleware(session_pool))

    dp.message.middleware(ThrottlingMiddleware(
        default_throttle_time=DEFAULT_THROTTLE_TIME))

    dp.message.middleware(InnerDatabaseMiddleware())
    dp.callback_query.middleware(InnerDatabaseMiddleware())

    dp.message.middleware(UserExistingMiddleware())

    dp.message.middleware(L10nMiddleware(translator_hub))
    dp.callback_query.middleware(L10nMiddleware(translator_hub))


# def setup_scheduling(
#         scheduler: AsyncIOScheduler,
#         bot: Bot,
#         config: Config,
#         translator_hub: TranslatorHub,
#         session_pool: async_sessionmaker
# ):


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Bot started!")


async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))

    # Localization initialization:
    locales_dir_path = Path(__file__).parent.joinpath("data/l10n/locales")
    translator_hub = setup_translator(locales_dir_path=str(locales_dir_path))

    # Routers and dialogs initialization:
    dp = Dispatcher(storage=storage)
    dp.include_routers(*routers_list)
    # setup_dialogs(dp)
    dp.workflow_data.update(config=config, translator_hub=translator_hub)

    # Database initialization:
    engine = create_engine(db=config.db)
    session_pool = create_session_pool(engine=engine)

    # Middlewares initialization:
    register_global_middlewares(
        dp=dp,
        translator_hub=translator_hub,
        session_pool=session_pool
    )

    # Scheduling initialization:
    # scheduler = AsyncIOScheduler()
    # setup_scheduling()

    await on_startup(bot, config.tg_bot.admin_ids)
    # scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Stopping bot")
