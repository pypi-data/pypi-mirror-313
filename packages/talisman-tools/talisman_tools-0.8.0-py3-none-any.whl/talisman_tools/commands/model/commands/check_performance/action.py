import logging
import time
from collections import defaultdict
from typing import Any, Callable

from tdm import TalismanDocument

from tp_interfaces.abstract import AbstractDocumentProcessor


logger = logging.getLogger(__name__)


def measure_default(f: Callable):
    def wrapper(*args, **kwargs) -> dict[str, float]:
        start_time = time.time()
        f(*args, **kwargs)
        end_time = time.time()

        return {'time': end_time - start_time}
    return wrapper


def measure_linux(f: Callable[[Any], dict[str, float]]):  # throws ImportError if resource is not available on the platform
    import resource

    def wrapper(*args, **kwargs) -> dict[str, float]:
        start_usage = resource.getrusage(resource.RUSAGE_SELF)
        res = f(*args, **kwargs)
        end_usage = resource.getrusage(resource.RUSAGE_SELF)

        res['ru_maxrss'] = end_usage.ru_maxrss  # there is no way to reset max_rss tracker
        res['ru_utime'] = end_usage.ru_utime - start_usage.ru_utime
        res['ru_stime'] = end_usage.ru_stime - start_usage.ru_stime
        return res
    return wrapper


def measure_torch(f: Callable[[Any], dict[str, float]]):  # throws ImportError if torch is not available
    import torch

    def wrapper(*args, **kwargs) -> dict[str, float]:
        res = f(*args, **kwargs)

        if not torch.cuda.is_available():
            return res

        for device in range(torch.cuda.device_count()):
            torch.cuda.init()  # for some reason without it stats is an empty dict
            stats = torch.cuda.memory_stats()

            res[f'device.{device}.peak_reserved'] = stats['reserved_bytes.all.peak']
            res[f'device.{device}.peak_allocated'] = stats['allocated_bytes.all.peak']
            torch.cuda.reset_peak_memory_stats()
        return res
    return wrapper


async def async_measure(docs: tuple[TalismanDocument, ...], model: AbstractDocumentProcessor, count: int):
    async with model:
        measure(docs, model, count)


def measure(docs: tuple[TalismanDocument, ...], model: AbstractDocumentProcessor, count: int):
    def runner():
        config_type = model.config_type
        model.process_docs(docs, config_type())

    _measure = measure_default(runner)

    try:
        _measure = measure_linux(_measure)
    except ImportError:
        logger.warning('Ignoring Linux metrics.')

    try:
        _measure = measure_torch(_measure)
    except ImportError:
        logger.warning('Ignoring CUDA metrics.')

    average_metrics = defaultdict(float)

    for run_idx in range(count):
        for metric_name, metric_value in _measure().items():
            average_metrics[metric_name] += metric_value
            logger.info(f'[Run {run_idx}] {metric_name}: {metric_value}')

    for metric_name, metric_value in average_metrics.items():
        logger.info(f'[Average] {metric_name}: {metric_value / count}')
