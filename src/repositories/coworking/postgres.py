import psycopg2
import typing as tp
import datetime as dt
from .base import CoworkingRepositoryBase
from .models import COWORKING_STATUS, CoworkingStatus


class CoworkingRepositoryPostgres(CoworkingRepositoryBase):
    def __init__(self, connection: psycopg2.extensions.connection) -> None:
        self.conn = connection

    def get_status(
        self,
    ) -> CoworkingStatus | None:
        cur = self.conn.cursor()
        cur.execute(
            """
                select 
                    tu.id,
                    tu.first_name,
                    tu.username,
                    cw.status,
                    cw.duration,
                    cw.created_at 
                from coworking cw 
                join telegram_users tu 
                on cw.responsible_id = tu.id 
                order by cw.created_at desc limit 1;
            """
        )
        result = cur.fetchone()
        if result is None:
            return None
        tg_id, first_name, username, status, duration, created_at = result
        mention = (
            f"@{username}"
            if username is not None
            else f"[{first_name}](tg://user?id={tg_id})"
        )

        cur.close()
        return CoworkingStatus(
            responsible_mention=mention,
            status=status,
            duration=duration,
            time=created_at,
        )

    def set_status(
        self,
        tg_id: int,
        status: tp.Annotated[str, COWORKING_STATUS],
        duration: int | None = None,
    ) -> None:
        if status not in ("open", "close"):
            raise ValueError("Invalid status value (must be 'open' or 'close')")
        if duration is not None and duration < 0:
            raise ValueError("Invalid duration value (must be positive)")

        cur = self.conn.cursor()
        cur.execute(
            "insert into coworking(responsible_id, status, duration, created_at) values (%s, %s, %s, %s);",
            (tg_id, status, duration, dt.datetime.now()),
        )
        self.conn.commit()
        cur.close()
