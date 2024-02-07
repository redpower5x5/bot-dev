import asyncio
import typing as tp
from aiogram import Bot, types, Router, F

from aiogram.filters import and_f
from aiogram.utils.i18n import gettext as _

from controllers.coworking import CoworkingController
from repositories.coworking.models import CoworkingStatus, COWORKING_STATUS

from repositories.users.models import TelegramUser

import datetime as dt


from ..keyboards.menu import (
    coworking_menu_keyboard,
    MainMenuCallback,
    CoworkingMenuCallback,
    SubscriptionCallback,
)
# from ..keyboards.coworking import coworking_subscription,
from ..keyboards.coworking_admin import (
    CoworkingStatusCallback,
    coworking_admin_keyboard,
)
from utils import get_user_mention

router: tp.Final[Router] = Router(name="coworking")


@router.callback_query(MainMenuCallback.filter(F.next_menu_prefix == "coworking"))
async def coworking_menu(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
    ) -> None:
    msg_text = _("coworking menu text")
    subscribed = coworking_controller.is_subscribed(tg_user.tg_id)
    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, subscribed),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, subscribed),
        )


# @router.callback_query(CoworkingMenuCallback.filter(F.action == "info"))
# async def coworking_info(callback: types.CallbackQuery, tg_user: TelegramUser) -> None:
#     msg_text = _("coworking info text")

#     if callback.message:
#         await callback.message.edit_text(
#             msg_text,
#             reply_markup=coworking_menu_keyboard(tg_user.is_admin),
#         )
#     else:
#         await callback.answer(
#             msg_text,
#             reply_markup=coworking_menu_keyboard(tg_user.is_admin),
#         )


@router.callback_query(CoworkingMenuCallback.filter(F.action == "status"))
async def coworking_status(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:
    status: CoworkingStatus | None = coworking_controller.get_status()
    subscribed = coworking_controller.is_subscribed(tg_user.tg_id)

    if status is None:
        msg_text = _("coworking status text if status is None")
    else:
        if status.duration:
            msg_text = _("coworking closed until {due} {mention}").format(
                due=dt.datetime.strftime(status.time+dt.timedelta(minutes=status.duration), "%H:%M"),
                mention=status.responsible_mention
            )
        else:
            if status.status == 'open':
                msg_text = _("coworking open {mention}").format(mention=status.responsible_mention)
            else: msg_text = _("coworking closed {mention}").format(mention=status.responsible_mention)

    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, subscribed),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, subscribed),
        )


# @router.callback_query(CoworkingMenuCallback.filter(F.action == "subscribe"))
# async def coworking_notifications(
#     callback: types.CallbackQuery,
#     tg_user: TelegramUser,
#     coworking_controller: CoworkingController,
# ) -> None:
#     msg_text = _(
#         "Подписавшись на обновления тебе будут приходить уведомление о статусе коворкинга"
#     )
#     subscribed = coworking_controller.is_subscribed(tg_user.tg_id)
#     if callback.message:
#         await callback.message.edit_text(
#             msg_text,
#             reply_markup=coworking_subscription(subscribed),
#         )
#     else:
#         await callback.answer(
#             msg_text,
#             reply_markup=coworking_subscription(subscribed),
#         )


@router.callback_query(SubscriptionCallback.filter(F.subscribed == True))
async def coworking_unsubscribe(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:
    msg_text = _("Ты отписался от уведомлений о статусе коворкинга")
    coworking_controller.subscribe_user(tg_user.tg_id, False)

    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, False),
        )
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, False),
        )


@router.callback_query(SubscriptionCallback.filter(F.subscribed == False))
async def coworking_subscribe(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
) -> None:

    msg_text = _("Ты подписался на уведомления о статусе коворкинга")

    coworking_controller.subscribe_user(tg_user.tg_id, True)

    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, True),
        )
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_menu_keyboard(tg_user.is_admin, True),
        )


@router.callback_query(CoworkingMenuCallback.filter(F.action == "admin_menu"))
async def coworking_admin_menu(callback: types.CallbackQuery) -> None:
    msg_text = _("coworking admin menu text")

    if callback.message:
        await callback.message.edit_text(
            msg_text,
            reply_markup=coworking_admin_keyboard(CoworkingStatusCallback()),
        )
    else:
        await callback.answer(
            msg_text,
            reply_markup=coworking_admin_keyboard(CoworkingStatusCallback()),
        )


@router.callback_query(CoworkingStatusCallback.filter(F.action == None))
async def coworking_status_menu(
    callback: types.CallbackQuery,
    callback_data: CoworkingStatusCallback,
) -> None:
    msg_text = _("Меню администратора для управления статусом ковркинга")
    markup = coworking_admin_keyboard(callback_data)
    if callback.message:
        await callback.message.edit_text(msg_text, reply_markup=markup)
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=markup,
        )


@router.callback_query(
    and_f(
        CoworkingStatusCallback.filter(F.action == CoworkingStatus.CLOSE),
        CoworkingStatusCallback.filter(F.duration == None),
    )
)
async def coworking_status_duration_selector(
    callback: types.CallbackQuery,
    callback_data: CoworkingStatusCallback,
) -> None:
    msg_text = _("Coworking admin status close durations selection")
    markup = coworking_admin_keyboard(callback_data)
    if callback.message:
        await callback.message.edit_text(msg_text, reply_markup=markup)
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=markup,
        )


@router.callback_query(
    CoworkingStatusCallback.filter(
        F.action == CoworkingStatus.CLOSE and F.duration != None
    )
)
async def coworking_status_close(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
    callback_data: CoworkingStatusCallback,
    bot: Bot,
) -> None:

    coworking_controller.set_status(
        tg_user.tg_id,
        callback_data.action,  # type: ignore ( т.к. проверяем в фильтре)
        callback_data.duration if callback_data.duration > 0 else None,  # type: ignore ( т.к. проверяем в фильтре)
    )
    mention = get_user_mention(tg_user)
    if callback_data.duration == -1:
        msg_text = _("🔑🔴 Коворкинг ITAM закрыт \n\nОтветственный: {mention}").format(
            mention=mention
        )
    else:

        msg_text = _(
            "🔑🔴 Коворкинг ITAM закрыт на {duration} минут \n\nОтветственный: {mention}"
        ).format(duration=callback_data.duration, mention=mention)
    markup = coworking_admin_keyboard(callback_data)
    if callback.message:
        await callback.message.edit_text(msg_text, reply_markup=markup)
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=markup,
        )

    # уведомление пользователей об изменении статуса коворкинга
    subscribed = coworking_controller.get_subscribed_ids()
    print(subscribed)
    for i in subscribed:
        await asyncio.sleep(0.2)
        await bot.send_message(i, msg_text)
    # await asyncio.gather(*[bot.send_message(u_id, msg_text) for u_id in subscribed])


@router.callback_query(CoworkingStatusCallback.filter(F.action == CoworkingStatus.OPEN))
async def coworking_status_open(
    callback: types.CallbackQuery,
    tg_user: TelegramUser,
    coworking_controller: CoworkingController,
    callback_data: CoworkingStatusCallback,
    bot: Bot,
) -> None:

    coworking_controller.set_status(tg_user.tg_id, callback_data.action)  # type: ignore проверено в фильтре
    mention = get_user_mention(tg_user)

    msg_text = _("🟢 Коворкинг ITAM открыт \n\nОтветственный: {mention}").format(
        mention=mention
    )
    markup = coworking_admin_keyboard(callback_data)
    if callback.message:
        await callback.message.edit_text(msg_text, reply_markup=markup)
        await callback.answer()
    else:
        await callback.answer(
            msg_text,
            reply_markup=markup,
        )

    # уведомление пользователей об изменении статуса коворкинга
    subscribed = coworking_controller.get_subscribed_ids()
    print(subscribed)
    print(subscribed)
    for i in subscribed:
        await asyncio.sleep(0.2)
        await bot.send_message(i, msg_text)
    # await asyncio.gather(*[bot.send_message(u_id, msg_text) for u_id in subscribed])
