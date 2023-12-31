import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n


import psycopg2
import dotenv
from .middlewares import UserMiddleware, CoworkingMiddleware, Localization

# FIXME: merging routers
from .handlers import common, coworking

from repositories.coworking import CoworkingRepositoryPostgres
from repositories.users import UserRepositoryPostgres
from controllers.coworking import CoworkingController

dotenv.load_dotenv("../.env")


TOKEN = "6509452055:AAHlGf_B0g4EHuIZRHre7aUaIxW7BpEy39g"
PG_HOST = getenv("POSTGRES_HOST")
PG_DB = getenv("POSTGRES_DB")
PG_USER = getenv("POSTGRES_USER")
PG_PASSWORD = getenv("POSTGRES_PASSWORD")

if (
    TOKEN is None
    or PG_HOST is None
    or PG_DB is None
    or PG_USER is None
    or PG_PASSWORD is None
):
    raise ValueError("Missing environment variables")


async def main() -> None:
    # TODO: separate router creation
    pg_connection = psycopg2.connect(
        host=PG_HOST, database=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    user_repo = UserRepositoryPostgres(pg_connection)
    coworking_repo = CoworkingRepositoryPostgres(pg_connection)
    i18n = I18n(path="translations", default_locale="ru", domain="messages")

    dp = Dispatcher()
    locale = Localization(i18n)
    locale.setup(dp)

    dp.update.outer_middleware(UserMiddleware(user_repo))

    dp.update.outer_middleware(CoworkingMiddleware(user_repo, coworking_repo))
    dp.include_routers(common.router, coworking.router)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)
