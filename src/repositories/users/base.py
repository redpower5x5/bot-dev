from abc import ABC, abstractmethod
from .models import TelegramUser


class UserRepositoryBase(ABC):
    @abstractmethod
    def save_user(
        self,
        tg_id: int,
        first_name: str,
        last_name: str | None,
        username: str | None,
        is_premium: bool = False,
        language_code: str = "ru",
        is_admin: bool = False,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, tg_id: int) -> TelegramUser | None:
        raise NotImplementedError

    @abstractmethod
    def get_users(self, limit: int = 10, offset: int = 0) -> list[TelegramUser]:
        raise NotImplementedError

    @abstractmethod
    def save_user(
        self,
        tg_id: int,
        first_name: str,
        last_name: str | None,
        username: str | None,
        is_premium: bool = False,
        language_code: str = "ru",
        is_admin: bool | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_admin(self, tg_id: int) -> bool:
        raise NotImplementedError
