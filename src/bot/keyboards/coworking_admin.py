import typing as tp
from aiogram import types

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from bot.keyboards.menu import MainMenuCallback

from repositories.coworking.models import CoworkingStatus, COWORKING_STATUS


class CoworkingStatusCallback(CallbackData, prefix="coworking_status"):
    action: tp.Optional[COWORKING_STATUS] = None
    duration: tp.Optional[int] = None


def coworking_admin_keyboard(
    coworking_data: CoworkingStatusCallback,
) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    match coworking_data.action:
        case None:
            builder.button(
                text=_("Открыть коворкинг"),
                callback_data=CoworkingStatusCallback(action=CoworkingStatus.OPEN),
            )
            builder.button(
                text=_("Coworking admin status change to close inline keyboard button"),
                callback_data=CoworkingStatusCallback(action=CoworkingStatus.CLOSE),
            )
            builder.adjust(1)
        case CoworkingStatus.OPEN:
            builder.button(
                text=_("Открыть коворкинг"),
                callback_data=CoworkingStatusCallback(action=CoworkingStatus.OPEN),
            )
            builder.button(
                text=_("Coworking admin status change to close inline keyboard button"),
                callback_data=CoworkingStatusCallback(action=CoworkingStatus.CLOSE),
            )
            builder.adjust(1)
        case CoworkingStatus.CLOSE:
            if coworking_data.duration is None:
                builder.button(
                    text=_("Закрыть до завтра"),
                    callback_data=CoworkingStatusCallback(
                        action=CoworkingStatus.CLOSE, duration=-1
                    ),
                )

                builder.button(
                    text=_("🚧 на 30 минут"),
                    callback_data=CoworkingStatusCallback(
                        action=CoworkingStatus.CLOSE, duration=30
                    ),
                )
                builder.button(
                    text=_("🚧 на 60 минут"),
                    callback_data=CoworkingStatusCallback(
                        action=CoworkingStatus.CLOSE, duration=60
                    ),
                )
                builder.adjust(1)

            else:
                builder.button(
                    text=_("Открыть коворкинг"),
                    callback_data=CoworkingStatusCallback(action=CoworkingStatus.OPEN),
                )
                builder.button(
                    text=_("Закрыть коворкинг"),
                    callback_data=CoworkingStatusCallback(action=CoworkingStatus.CLOSE),
                )
                builder.adjust(1)

    builder.button(
        text=_("↩️ Назад"),
        callback_data=MainMenuCallback(next_menu_prefix="coworking"),
    )
    return builder.as_markup()
