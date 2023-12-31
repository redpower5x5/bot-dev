import datetime as dt

from repositories.coworking import CoworkingRepositoryBase
from repositories.users import UserRepositoryBase
from repositories.coworking.models import CoworkingStatus


class CoworkingController:
    def __init__(
        self, coworking_repo: CoworkingRepositoryBase, user_repo: UserRepositoryBase
    ) -> None:
        self.coworking_repo = coworking_repo
        self.user_repo = user_repo

    def get_status(self) -> CoworkingStatus | None:
        return self.coworking_repo.get_status()

    def set_status(
        self, tg_id: int, status: str, duration: int | None = None
    ) -> CoworkingStatus:
        user = self.user_repo.get_user(tg_id)
        if user is None or not user.is_admin:
            raise ValueError("user is not admin")

        self.coworking_repo.set_status(tg_id, status, duration)
        mention = (
            f"@{user.username}"
            if user.username is not None
            else f"[{user.first_name}](tg://user?id={tg_id})"
        )
        return CoworkingStatus(
            responsible_mention=mention,
            status=status,
            duration=duration,
            time=dt.datetime.now(),
        )
