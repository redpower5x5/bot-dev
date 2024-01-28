from email import message
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from aiogram.utils.i18n import I18n


import psycopg2
import dotenv


from .middlewares import (
    UserMiddleware,
    CoworkingMiddleware,
    Localization,
    SettingsMiddleware,
    BotMiddleware,
)


from .handlers import common, coworking, profile

from repositories.coworking import CoworkingRepositoryPostgres
from repositories.users import UserRepositoryPostgres
from .settings import Settings

dotenv.load_dotenv("../.env")


async def main() -> None:
    settings = Settings()  # type: ignore
    pg_connection = psycopg2.connect(settings.build_postgres_dsn())

    user_repo = UserRepositoryPostgres(pg_connection)
    coworking_repo = CoworkingRepositoryPostgres(pg_connection)
    i18n = I18n(path="translations", default_locale="ru", domain="messages")

    dp = Dispatcher()
    bot = Bot(settings.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    locale = Localization(i18n)
    locale.setup(dp)

    dp.update.outer_middleware(SettingsMiddleware(settings))
    dp.update.outer_middleware(BotMiddleware(bot))
    dp.update.outer_middleware(UserMiddleware(user_repo))

    dp.update.middleware(CoworkingMiddleware(user_repo, coworking_repo))
    dp.include_routers(common.router, coworking.router, profile.router)

    admins = user_repo.get_admins()

    # for user_id in admins:
    #     await bot.send_message(
    #         chat_id=user_id,
    #         text="Бот был перезапущен, подписки на коворкинг сброшены",
    #     )

    await dp.start_polling(bot)
