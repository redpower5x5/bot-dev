import typing as tp
import datetime as dt
from .models import CoworkingStatus
from abc import ABC, abstractmethod


class CoworkingRepositoryBase(ABC):
    @abstractmethod
    def get_status(
        self,
    ) -> CoworkingStatus | None:
        raise NotImplementedError

    @abstractmethod
    def set_status(self, tg_id: int, status: str, duration: int | None = None) -> None:
        raise NotImplementedError
