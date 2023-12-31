import typing as tp

from aiogram import Router
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold
from aiogram.utils.i18n import gettext as _
from ..keyboards.menu import menu_keyboard

from repositories.users.models import TelegramUser

router: tp.Final[Router] = Router(name="common")


@router.message(CommandStart())
async def command_start_handler(message: types.Message, user: TelegramUser) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    if message.from_user is None:
        return

    username = hbold(user.username or user.first_name)
    await message.answer(
        text=_("Hello , {username}!").format(username=username),
        reply_markup=menu_keyboard(),
    )
