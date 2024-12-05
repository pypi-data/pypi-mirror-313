from functools import lru_cache
from logging import Logger


@lru_cache(None)
def warn_once(logger: Logger, msg: str, **kwargs):
    logger.warning(msg, **kwargs)
