import psycopg2
import typing as tp
import datetime as dt
from .base import UserRepositoryBase
from .models import TelegramUser


class UserRepositoryPostgres(UserRepositoryBase):
    def __init__(self, connection: psycopg2.extensions.connection) -> None:
        self.conn = connection

    def get_user(self, tg_id: int) -> TelegramUser | None:
        cur = self.conn.cursor()
        cur.execute(
            """
                select 
                    id,
                    first_name,
                    last_name,
                    username,
                    is_premium,
                    language_code,
                    is_admin
                from telegram_users
                where id = %s;
            """,
            (tg_id,),
        )
        result = cur.fetchone()
        if result is None:
            return None
        (
            tg_id,
            first_name,
            last_name,
            username,
            is_premium,
            language_code,
            is_admin,
        ) = result
        cur.close()
        return TelegramUser(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_premium=is_premium,
            language_code=language_code,
            is_admin=is_admin,
        )

    def get_users(self, limit: int = 10, offset: int = 0) -> list[TelegramUser]:
        cur = self.conn.cursor()
        cur.execute(
            """
                select 
                    id,
                    first_name,
                    last_name,
                    username,
                    is_premium,
                    language_code,
                    is_admin
                from telegram_users
                order by id
                limit %s offset %s;
            """,
            (limit, offset),
        )
        result = cur.fetchall()
        cur.close()
        return [
            TelegramUser(
                tg_id=tg_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                is_premium=is_premium,
                language_code=language_code,
                is_admin=is_admin,
            )
            for (
                tg_id,
                first_name,
                last_name,
                username,
                is_premium,
                language_code,
                is_admin,
            ) in result
        ]

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
        """
        replace old user data with new one if user already exists other wise create new user
        """
        cur = self.conn.cursor()
        if is_admin is None:
            cur.execute(
                """
                    insert into telegram_users (
                        id,
                        first_name,
                        last_name,
                        username,
                        is_premium,
                        language_code
                    ) values (%s, %s, %s, %s, %s, %s)
                    on conflict (id) do update set
                        first_name = excluded.first_name,
                        last_name = excluded.last_name,
                        username = excluded.username,
                        is_premium = excluded.is_premium,
                        language_code = excluded.language_code;
                """,
                (tg_id, first_name, last_name, username, is_premium, language_code),
            )
        else:
            cur.execute(
                """
                    insert into telegram_users (
                        id,
                        first_name,
                        last_name,
                        username,
                        is_premium,
                        language_code,
                        is_admin
                    ) values (%s, %s, %s, %s, %s, %s, %s)
                    on conflict (id) do update set
                        first_name = excluded.first_name,
                        last_name = excluded.last_name,
                        username = excluded.username,
                        is_premium = excluded.is_premium,
                        language_code = excluded.language_code,
                        is_admin = excluded.is_admin;
                """,
                (
                    tg_id,
                    first_name,
                    last_name,
                    username,
                    is_premium,
                    language_code,
                    is_admin,
                ),
            )
        self.conn.commit()
        cur.close()

    def is_admin(self, tg_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute(
            """
                select is_admin
                from telegram_users
                where id = %s;
            """,
            (tg_id,),
        )
        result = cur.fetchone()
        if result is None:
            return False
        is_admin = result[0]
        cur.close()
        return is_admin
