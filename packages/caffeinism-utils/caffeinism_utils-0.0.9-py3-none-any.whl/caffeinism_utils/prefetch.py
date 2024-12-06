from concurrent.futures import ThreadPoolExecutor

from .asyncio import run_in_executor
from .utils import DummyStopIteration, next_without_stop_iteration


def prefetch_iterator(iterator):
    with ThreadPoolExecutor(1) as p:
        iterator = iter(iterator)
        prefetched = p.submit(next, iterator)
        while True:
            try:
                rets = prefetched.result()
            except StopIteration:
                break
            prefetched = p.submit(next, iterator)
            yield rets


async def aprefetch_iterator(iterator):
    with ThreadPoolExecutor(1) as p:
        iterator = iter(iterator)
        prefetched = run_in_executor(p, next_without_stop_iteration, iterator)
        while True:
            try:
                ret = await prefetched
            except DummyStopIteration:
                break
            prefetched = run_in_executor(p, next_without_stop_iteration, iterator)
            yield ret
