from sqlite3 import SQLITE_CREATE_INDEX
import typing as tp
from aiogram import types

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

COWORKING_ACTIONS = tp.Literal[
    "info", "status", "subscribe", "unsubscribe", "admin_menu"
]

AVALIABLE_MENUS = tp.Literal["menu", "coworking", "profile", "help", "clubs"]

AVALIABLE_CLUBS = tp.Literal["hack_club", "design_club", "gamedev_club", "ai_club", "robot_club"]


class MainMenuCallback(CallbackData, prefix="menu"):
    next_menu_prefix: AVALIABLE_MENUS = "menu"


class CoworkingMenuCallback(CallbackData, prefix="coworking"):
    action: COWORKING_ACTIONS

class ClubsMenuCallback(CallbackData, prefix="clubs"):
    club: AVALIABLE_CLUBS


def menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("👥 Коворкинг"),
            callback_data=MainMenuCallback(next_menu_prefix="coworking").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("🏢 Клубы"),
            callback_data=MainMenuCallback(next_menu_prefix="clubs").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("⚙️ Профиль"),
            callback_data=MainMenuCallback(next_menu_prefix="profile").pack(),
        ),
    )
    # builder.row(
    #     types.InlineKeyboardButton(
    #         text=_("🆘 Что это такое?"),
    #         callback_data=MainMenuCallback(next_menu_prefix="help").pack(),
    #     ),
    # )

    return builder.as_markup()


def coworking_menu_keyboard(is_admin: bool) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("ℹ️ Информация"),
            callback_data=CoworkingMenuCallback(action="info").pack(),
        ),
        types.InlineKeyboardButton(
            text=_("📝 Статус"),
            callback_data=CoworkingMenuCallback(action="status").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("✉️ Обновления"),
            callback_data=CoworkingMenuCallback(action="subscribe").pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("↩️ Назад"),
            callback_data=MainMenuCallback(next_menu_prefix="menu").pack(),
        )
    )
    if is_admin:
        builder.row(
            types.InlineKeyboardButton(
                text=_("🔧 Меню администратора"),
                callback_data=CoworkingMenuCallback(action="admin_menu").pack(),
            ),
        )

    return builder.as_markup()

def clubs_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("🖥️ Хакатон клуб"),
            callback_data=ClubsMenuCallback(club="hack_club").pack(),
        ),
        types.InlineKeyboardButton(
            text=_("🎨 Design клуб"),
            callback_data=ClubsMenuCallback(club="design_club").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("🎮 Gamedev клуб"),
            callback_data=ClubsMenuCallback(club="gamedev_club").pack(),
        ),
        types.InlineKeyboardButton(
            text=_("🧠 AI Knowledge клуб"),
            callback_data=ClubsMenuCallback(club="ai_club").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("🤖 клуб робототехники"),
            callback_data=ClubsMenuCallback(club="robot_club").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("↩️ Назад"),
            callback_data=MainMenuCallback(next_menu_prefix="menu").pack(),
        )
    )

    return builder.as_markup()
