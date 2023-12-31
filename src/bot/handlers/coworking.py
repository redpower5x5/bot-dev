# TODO: add previus steps into callbackdata and add back button

import typing as tp
from aiogram import types, Router, F
from aiogram.utils.i18n import gettext as _
from controllers.coworking import CoworkingController
from repositories.coworking.models import CoworkingStatus

from repositories.users.models import TelegramUser

from ..keyboards.menu import (
    coworking_menu_keyboard,
    coworking_status_keyboard,
    coworking_close_duration,
)

router: tp.Final[Router] = Router(name="coworking")

# TODO: change callback data into classes with data
@router.callback_query(F.data == "coworking_menu")
async def coworking_menu(callback: types.CallbackQuery, user: TelegramUser) -> None:
    print(user)
    if callback.message:
        await callback.message.edit_text(
            _("coworking menu text"),
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
    else:
        await callback.answer(
            _("coworking menu text"),
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )


# TODO: change callback data into classes with data
@router.callback_query(F.data == "coworking_info")
async def coworking_info(callback: types.CallbackQuery, user: TelegramUser) -> None:
    if callback.message:
        await callback.message.edit_text(
            _("coworking info text"),
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
    else:
        await callback.answer(
            _("coworking info text"),
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )


# TODO: change callback data into classes with data
@router.callback_query(F.data == "coworking_status")
async def coworking_status(
    callback: types.CallbackQuery,
    user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:
    status: CoworkingStatus | None = coworking_controller.get_status()
    print(status)
    if status is None:
        msg_text = _("coworking status text if status is None")
    else:
        if status.duration:
            msg_text = _("coworking status text {status} {duration}").format(
                status=status.status, duration=status.duration
            )
        else:
            msg_text = _("coworking status text {status}").format(status=status)

    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )


# TODO: make one handler for open and close status
@router.callback_query(F.data == "coworking_admin_menu")
async def coworking_admin_menu(
    callback: types.CallbackQuery, user: TelegramUser
) -> None:
    msg_text = _("coworking admin menu text")

    if callback.message:
        await callback.message.edit_text(
            _("coworking admin menu text"),
            reply_markup=coworking_status_keyboard(),
        )
    else:
        await callback.answer(
            _("coworking admin menu text"),
            reply_markup=coworking_status_keyboard(),
        )


# FIXME: merge into one handler
@router.callback_query(F.data == "coworking_status_open")
async def coworking_admin_status_open(
    callback: types.CallbackQuery,
    user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:
    coworking_controller.set_status(user.tg_id, CoworkingStatus.OPEN)
    msg_text = _("coworking status change to open text")
    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )


@router.callback_query(F.data == "coworking_status_close")
async def coworking_admin_status_close(
    callback: types.CallbackQuery,
) -> None:

    msg_text = _("coworking status change to close choose duration text")
    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_close_duration(),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_close_duration(),
        )


@router.callback_query(F.data.startswith("coworking_status_change_close_"))
async def coworking_admin_choose_duration(
    callback: types.CallbackQuery,
    user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:
    duration = callback.data.split("_")[-1]
    if duration == "permanent":
        duration = None
    else:
        duration = int(duration)
    coworking_controller.set_status(user.tg_id, CoworkingStatus.CLOSE, duration)
    msg_text = _("coworking status change to close text")
    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(user.is_admin),
        )
