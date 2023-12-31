import typing as tp
from aiogram import types
from aiogram.utils.i18n import I18nMiddleware

from repositories.users.models import TelegramUser


class Localization(I18nMiddleware):
    async def get_locale(
        self, event: types.TelegramObject, data: tp.Dict[str, tp.Any]
    ) -> str:

        if "event_from_user" in data.keys():

            return data["event_from_user"].language_code or "ru"

        return "ru"
