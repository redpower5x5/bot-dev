from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking inline keyboard button"), callback_data="coworking_menu"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("Settings inline keyboard button"), callback_data="settings"
        ),
    )
    return builder.as_markup()


def coworking_menu_keyboard(is_admin: bool) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking info inline keyboard button"),
            callback_data="coworking_info",
        ),
        types.InlineKeyboardButton(
            text=_("Coworking status inline keyboard button"),
            callback_data="coworking_status",
        ),
    )
    if is_admin:
        builder.row(
            types.InlineKeyboardButton(
                text=_("Coworking admin menu inline keyboard button"),
                callback_data="coworking_admin_menu",
            ),
        )

    return builder.as_markup()


def coworking_status_keyboard() -> types.InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking admin status change to open inline keyboard button"),
            callback_data="coworking_status_open",
        ),
        types.InlineKeyboardButton(
            text=_("Coworking admin status change to close inline keyboard button"),
            callback_data="coworking_status_close",
        ),
    )

    return builder.as_markup()


def coworking_close_duration() -> types.InlineKeyboardMarkup:
    # FIXME: make callbackdata class for different durations
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking admin close duration permanent  inline keyboard button"),
            callback_data="coworking_status_change_close_permanent",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking admin close duration 30 minutes inline keyboard button"),
            callback_data="coworking_status_change_close_30",
        ),
        types.InlineKeyboardButton(
            text=_("Coworking admin close duration 60 minutes inline keyboard button"),
            callback_data="coworking_status_change_close_60",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=_("Coworking admin close duration 90 minutes inline keyboard button"),
            callback_data="coworking_status_change_close_90",
        ),
        types.InlineKeyboardButton(
            text=_("Coworking admin close duration 120 minutes inline keyboard button"),
            callback_data="coworking_status_change_close_120",
        ),
    )

    return builder.as_markup()
