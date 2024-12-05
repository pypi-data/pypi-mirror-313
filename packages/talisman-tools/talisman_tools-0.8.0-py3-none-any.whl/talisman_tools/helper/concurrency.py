from multiprocessing.pool import ApplyResult
from typing import Callable, Dict, TypeVar

from anyio import Semaphore
from starlette.concurrency import run_in_threadpool

from talisman_tools.helper.env import get_max_concurrent_threads, get_max_treated_jobs

MAX_CONCURRENT_THREADS = get_max_concurrent_threads()
MAX_THREADS_GUARD = Semaphore(MAX_CONCURRENT_THREADS)
_AnyResult = TypeVar('_AnyResult')


async def execute_concurrently(io_bound_fn: Callable[[], _AnyResult]) -> _AnyResult:
    # too many threads may degrade the performance
    async with MAX_THREADS_GUARD:
        return await run_in_threadpool(io_bound_fn)


def check_on_jobs(decoding_jobs: Dict[int, ApplyResult[_AnyResult]], *, ignore_max_treated_jobs: bool = False) -> Dict[int, _AnyResult]:
    completed = []
    results = {}
    for job_id, job in decoding_jobs.items():
        if job.ready():
            results[job_id] = job.get()
            completed.append(job_id)

        if not ignore_max_treated_jobs and len(completed) >= get_max_treated_jobs():
            break

    for job_id in completed:
        decoding_jobs.pop(job_id)

    return results
