import asyncio
from functools import partial


def run_in_threadpool(func, *args, **kwargs):
    return run_in_executor(None, func, *args, **kwargs)


def run_in_executor(pool, func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    func = partial(func, *args, **kwargs)
    return loop.run_in_executor(pool, func)
