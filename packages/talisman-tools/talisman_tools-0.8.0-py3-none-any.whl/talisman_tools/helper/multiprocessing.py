import os

MULTIPROCESSING_SETUP = False


def setup_multiprocessing():
    """Conventional forking is not safe in multithreaded environment. Use this function in __main__ to set up thread-safe version
    of spawning new processes.

    See https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
    """
    global MULTIPROCESSING_SETUP
    if MULTIPROCESSING_SETUP:
        return

    try:
        import torch.multiprocessing as multiprocessing
    except ImportError:
        import multiprocessing

    multiprocessing.set_start_method('spawn' if os.name == 'nt' else 'forkserver', force=True)
    MULTIPROCESSING_SETUP = True
