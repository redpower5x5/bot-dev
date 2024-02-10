from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError
from controllers.coworking import CoworkingController
from repositories.coworking.models import CoworkingStatus, COWORKING_ACTIONS
import logging
from datetime import datetime as dt
from datetime import timedelta
import typing as tp

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

async def schedule_coworking_status(
        scheduler: AsyncIOScheduler,
        coworking_controller: CoworkingController,
        tg_id: int,
        status: CoworkingStatus) -> None:
    try:
        scheduler.add_job(
            coworking_controller.set_status,
            "date",
            run_date=dt.now() + timedelta(minutes=status.duration),
            args=[tg_id, status.status, None],
            id="coworking_status",
            replace_existing=True,
        )
        log.info("Coworking status scheduled")
    except JobLookupError:
        log.exception("Coworking status scheduling failed")

async def cancel_schedule_job(scheduler: AsyncIOScheduler, job_id: str) -> None:
    """
    Cancel scheduled broadcast

    :param scheduler:
    :param job_id:
    :return:
    """
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        log.error(f"Job {job_id} not found")
    else:
        log.info(f"Job {job_id} canceled")
