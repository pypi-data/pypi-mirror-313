from datetime import timedelta
from typing import IO, Any, List, Optional

from fused_batch._global_api import get_api
from fused_batch.models.internal.job import CoerceableToJobId, RunResponse


def job_get_logs(
    job: CoerceableToJobId,
    since_ms: Optional[int] = None,
) -> List[Any]:
    """Fetch logs for a job

    Args:
        job: the identifier of a job or a `RunResponse` object.
        since_ms: Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.

    Returns:
        Log messages for the given job.
    """
    api = get_api()
    return api.get_logs(job=job, since_ms=since_ms)


def job_print_logs(
    job: CoerceableToJobId,
    since_ms: Optional[int] = None,
    file: Optional[IO] = None,
) -> None:
    """Fetch and print logs for a job

    Args:
        job: the identifier of a job or a `RunResponse` object.
        since_ms: Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.
        file: Where to print logs to. Defaults to sys.stdout.

    Returns:
        None
    """
    job = RunResponse.from_job_id(job)
    job.print_logs(since_ms=since_ms, file=file)


def job_tail_logs(
    job: CoerceableToJobId,
    refresh_seconds: float = 1,
    sample_logs: bool = True,
    timeout: Optional[float] = None,
    get_logs_retries: int = 1,
):
    """Continuously print logs for a job

    Args:
        job: the identifier of a job or a `RunResponse` object.
        refresh_seconds: how frequently, in seconds, to check for new logs. Defaults to 1.
        sample_logs: if true, print out only a sample of logs. Defaults to True.
        timeout: if not None, how long to continue tailing logs for. Defaults to None for indefinite.
        get_logs_retries: Number of additional retries for log requests. Defaults to 1.
    """
    api = get_api()
    return api.tail_logs(
        job=job,
        refresh_seconds=refresh_seconds,
        sample_logs=sample_logs,
        timeout=timeout,
        get_logs_retries=get_logs_retries,
    )


def job_get_status(job: CoerceableToJobId) -> RunResponse:
    """Fetch the status of a running job

    Args:
        job: the identifier of a job or a `RunResponse` object.

    Returns:
        The status of the given job.
    """
    api = get_api()
    return api.get_status(job=job)


def job_cancel(job: CoerceableToJobId) -> RunResponse:
    """Cancel an existing job

    Args:
        job: the identifier of a job or a `RunResponse` object.

    Returns:
        A new job object.
    """
    api = get_api()
    return api.cancel_job(job=job)


def job_get_exec_time(job: CoerceableToJobId) -> timedelta:
    """Determine the execution time of this job, using the logs.

    Returns:
        Time the job took. If the job is in progress, time from first to last log message is returned.
    """
    job = RunResponse.from_job_id(job)
    return job.get_exec_time()


def job_wait_for_job(
    job: CoerceableToJobId,
    poll_interval_seconds: float = 5,
    timeout: Optional[float] = None,
) -> RunResponse:
    """Block the Python kernel until this job has finished

    Args:
        poll_interval_seconds: How often (in seconds) to poll for status updates. Defaults to 5.
        timeout: The length of time in seconds to wait for the job. Defaults to None.

    Raises:
        TimeoutError: if waiting for the job timed out.

    Returns:
        The status of the given job.
    """
    api = get_api()
    return api.wait_for_job(
        job,
        poll_interval_seconds=poll_interval_seconds,
        timeout=timeout,
    )
