import logging

from arq.jobs import Job

from backend.lib.redis_client import get_arq_pool

logger = logging.getLogger(__name__)


async def enqueue_task(
    user_id: str,
    task: str,
    job_id: str | None = None,
) -> Job | None:
    client = await get_arq_pool()
    job = await client.enqueue_job(
        "process_task",  # Must match the task function name registered in worker.py
        user_id=user_id,
        task=task,
        _job_id=job_id,
    )

    if job is None:
        logger.info("Skipped duplicate job %s", job_id)
    else:
        logger.info("Enqueued job %s for user %s", job.job_id, user_id)

    return job
