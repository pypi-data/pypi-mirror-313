import asyncio
import anyio
import nest_asyncio
import inspect
import threading
import typing
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from contextvars import ContextVar, copy_context
from functools import partial, wraps
import tqdm
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
    AsyncIterator,
)
from uuid import UUID, uuid4
import sys

import anyio
import anyio.abc
import anyio.from_thread
import anyio.to_thread
import sniffio
from typing_extensions import Literal, ParamSpec, TypeGuard

import signal
import functools
from loguru import logger
# import threading

# from prefect.logging import get_logger

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")
F = TypeVar("F", bound=Callable[..., Any])
Async = Literal[True]
Sync = Literal[False]
A = TypeVar("A", Async, Sync, covariant=True)

# Global references to prevent garbage collection for `add_event_loop_shutdown_callback`
EVENT_LOOP_GC_REFS = {}

GLOBAL_THREAD_LIMITER: Optional[anyio.CapacityLimiter] = None

RUNNING_IN_RUN_SYNC_LOOP_FLAG = ContextVar("running_in_run_sync_loop", default=False)
RUNNING_ASYNC_FLAG = ContextVar("run_async", default=False)
BACKGROUND_TASKS: set[asyncio.Task] = set()
background_task_lock = threading.Lock()

# Thread-local storage to keep track of worker thread state
_thread_local = threading.local()


def get_thread_limiter():
    global GLOBAL_THREAD_LIMITER

    if GLOBAL_THREAD_LIMITER is None:
        GLOBAL_THREAD_LIMITER = anyio.CapacityLimiter(250)

    return GLOBAL_THREAD_LIMITER


def is_async_fn(
    func: Union[Callable[P, R], Callable[P, Awaitable[R]]],
) -> TypeGuard[Callable[P, Awaitable[R]]]:
    """
    Returns `True` if a function returns a coroutine.

    See https://github.com/microsoft/pyright/issues/2142 for an example use
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.iscoroutinefunction(func)


def is_async_gen_fn(func):
    """
    Returns `True` if a function is an async generator.
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__

    return inspect.isasyncgenfunction(func)


def create_task(coroutine: Coroutine) -> asyncio.Task:
    """
    Replacement for asyncio.create_task that will ensure that tasks aren't
    garbage collected before they complete. Allows for "fire and forget"
    behavior in which tasks can be created and the application can move on.
    Tasks can also be awaited normally.

    See https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
    for details (and essentially this implementation)
    """

    task = asyncio.create_task(coroutine)

    # Add task to the set. This creates a strong reference.
    # Take a lock because this might be done from multiple threads.
    with background_task_lock:
        BACKGROUND_TASKS.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(BACKGROUND_TASKS.discard)

    return task


def run_async(coroutine):
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If there's no current event loop, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Check if we're in a Jupyter notebook
    if "IPython" in sys.modules:
        # If so, apply nest_asyncio to allow nested use of event loops
        nest_asyncio.apply()

    # Now we can safely run our coroutine
    return loop.run_until_complete(coroutine)


async def _async_generator_timeout(async_gen, timeout):
    try:
        while True:
            try:
                item = await asyncio.wait_for(async_gen.__anext__(), timeout)
                yield item
            except StopAsyncIteration:
                break
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(
            "Generator didn't emit a new item within the specified timeout"
        )


T = TypeVar("T")

global_stop = threading.Event()


@overload
def async_iterator(
    func: Callable[..., AsyncIterator[T]],
) -> Callable[..., AsyncIterator[T]]: ...


@overload
def async_iterator(
    func: None = None, iteration_timeout: float | None = None
) -> Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]: ...


def async_iterator(
    func: Callable[..., AsyncIterator[T]] | None = None,
    iteration_timeout: float | None = None,
    use_global_stop: bool = False,
) -> (
    Callable[..., AsyncIterator[T]]
    | Callable[[Callable[..., AsyncIterator[T]]], Callable[..., AsyncIterator[T]]]
):
    def inner(
        async_iter_func: Callable[..., AsyncIterator[T]],
    ) -> Callable[..., AsyncIterator[T]]:
        @functools.wraps(async_iter_func)
        async def wrapper(*args, **kwargs) -> AsyncIterator[T]:
            stop_event = asyncio.Event() if not use_global_stop else global_stop
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGINT, stop_event.set)
            try:
                if iteration_timeout is not None:
                    async_gen = _async_generator_timeout(
                        async_iter_func(*args, **kwargs), iteration_timeout
                    )
                else:
                    async_gen = async_iter_func(*args, **kwargs)

                async for item in async_gen:
                    if stop_event.is_set():
                        break
                    yield item
                    await asyncio.sleep(0)
            except (KeyboardInterrupt, asyncio.CancelledError):
                # logger.debug("Received interrupt signal")
                stop_event.set()
                raise
            # except* Exception as e:
            #     for exc in e.exceptions:
            #         logger.error(exc)
            finally:
                # logger.info("Cleaning up...")
                loop.remove_signal_handler(signal.SIGINT)
                return

        return wrapper

    if func is not None:
        return inner(func)

    return inner


class FunctionWithStop(Callable):
    global_stop: asyncio.Event

    def __call__(self) -> None: ...


if TYPE_CHECKING:
    async_iterator: FunctionWithStop

setattr(async_iterator, "global_stop", global_stop)


T = TypeVar("T")


async def handle_signals(scope: anyio.abc.CancelScope):
    async with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
        async for signum in signals:
            print(f"Received signal: {signum}")
            scope.cancel()  # This cancels th


async def _run_with(
    fn: Callable[..., Awaitable[T]], idx: int, _stop: asyncio.Event, **kwargs
) -> tuple[int, T]:
    if _stop.is_set():
        return idx, None
    return idx, await fn(**kwargs)


async def map_as_completed(
    fn: Callable[..., Awaitable[T]],
    *inputs: dict[str, Any],
    name: str = None,
    progress: bool = True,
    return_exceptions: bool = True,
    progress_position: int = 0,
) -> list[T]:
    _stop = asyncio.Event()
    output = {}
    tasks: set[asyncio.Task[tuple[int, T]]] = set()
    name = name or fn.__name__
    async with asyncio.TaskGroup() as tg:
        for idx, input in enumerate(inputs):
            task = tg.create_task(_run_with(fn, idx, _stop, **input))
            tasks.add(task)

        for result in tqdm.tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc=name,
            disable=not progress,
            position=progress_position,
        ):
            try:
                if _stop.is_set():
                    break
                idx, value = await result
                output[idx] = value
            except (asyncio.CancelledError, KeyboardInterrupt):
                _stop.set()
                raise
            except Exception as e:
                if return_exceptions:
                    output[idx] = e
                else:
                    raise e

        return list(dict(sorted(output.items(), key=lambda x: x[0])).values())


async def run_with_semaphore(
    semaphore: asyncio.Semaphore,
    coro: typing.Coroutine,
):
    async with semaphore:
        return await coro
