import typing as tp
from aiogram import BaseMiddleware
from aiogram import types

# TODO: change repositories package structure of imports
from repositories.users import UserRepositoryBase
from repositories.coworking import CoworkingRepositoryBase


class UserMiddleware(BaseMiddleware):
    def __init__(self, user_repo: UserRepositoryBase) -> None:
        self.user_repo = user_repo

    async def __call__(
        self,
        handler: tp.Callable[
            [types.TelegramObject, tp.Dict[str, tp.Any]], tp.Awaitable[tp.Any]
        ],
        event: types.TelegramObject,
        data: tp.Dict[str, tp.Any],
    ) -> tp.Any:

        tg_user: tp.Optional[types.User] = data.get("event_from_user")
        if tg_user is None:
            return await handler(event, data)
        self.user_repo.save_user(
            tg_user.id,
            tg_user.first_name,
            tg_user.last_name,
            tg_user.username,
        )

        data["user"] = self.user_repo.get_user(tg_user.id) if tg_user else None
        result = await handler(event, data)

        return result
