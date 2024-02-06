import typing as tp
from aiogram import types

from .menu import MainMenuCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

class SubscriptionCallback(CallbackData, prefix="club_subscription"):
    subscribed: bool
    club: str

def club_subscription_and_info(subscribed: bool, club: str, club_link: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if subscribed:
        builder.row(
            types.InlineKeyboardButton(
                text=_("Отписаться"),
                callback_data=SubscriptionCallback(subscribed=False, club=club).pack(),
            )
        )
    else:
        builder.row(
            types.InlineKeyboardButton(
                text=_("Подписаться"),
                callback_data=SubscriptionCallback(subscribed=True, club=club).pack(),
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text=_("📢 Чат клуба"),
            url=club_link
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("↩️ Назад"),
            callback_data=MainMenuCallback(next_menu_prefix="clubs").pack(),
        )
    )

    return builder.as_markup()