from concurrent.futures import ThreadPoolExecutor

from .asyncio import run_in_executor
from .utils import DummyStopIteration, next_without_stop_iteration


def thread_zip(*iterators):
    with ThreadPoolExecutor(len(iterators)) as p:
        iterators = [iter(iterator) for iterator in iterators]
        prefetched = [p.submit(next, iterator) for iterator in iterators]
        while True:
            try:
                rets = [task.result() for task in prefetched]
            except StopIteration:
                break
            prefetched = [p.submit(next, iterator) for iterator in iterators]
            yield rets


async def athread_zip(*iterators):
    with ThreadPoolExecutor(len(iterators)) as p:
        iterators = [iter(iterator) for iterator in iterators]
        prefetched = [
            run_in_executor(p, next_without_stop_iteration, iterator)
            for iterator in iterators
        ]
        while True:
            try:
                rets = [await task for task in prefetched]
            except DummyStopIteration:
                break
            prefetched = [
                run_in_executor(p, next_without_stop_iteration, iterator)
                for iterator in iterators
            ]
            yield rets
