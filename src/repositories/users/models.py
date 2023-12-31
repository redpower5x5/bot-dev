from dataclasses import dataclass
import typing as tp


@dataclass
class TelegramUser:
    """Пользователь телеграма

    Attributes
    ----------
    tg_id : int
        id пользователя
    first_name : str
        имя пользователя
    last_name : str | None
        фамилия пользователя
    username : str | None
        юзернейм пользователя
    is_premium : bool
        является ли пользователь премиумом
    language_code : str
        код языка пользователя
    is_admin : bool
        является ли пользователь админом
    """

    tg_id: int
    first_name: str
    last_name: str | None
    username: str | None
    is_premium: bool
    language_code: str
    is_admin: bool
