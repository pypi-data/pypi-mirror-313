import asyncio
import time
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar, Union

from opentelemetry import trace

from pyback.logger import logger

P = ParamSpec("P")
R = TypeVar("R")


def telemetry_decorator(
    func: Callable[P, Union[Coroutine[Any, Any, R], R]]
) -> Callable[P, Union[Coroutine[Any, Any, R], Union[R, Coroutine[Any, Any, R]]]]:
    """
    A decorator that adds telemetry to a function. It logs the execution time and traces the function execution.

    Args:
        func (Callable[P, Union[Coroutine[Any, Any, R], R]]): The function to be decorated.

    Returns:
        Callable[P, Union[Coroutine[Any, Any, R], Union[R, Coroutine[Any, Any, R]]]]: The decorated function.
    """

    def log_execution(func_name: str, duration: float) -> None:
        logger.debug(f"{func_name} function performed in {duration} seconds.")

    def trace_execution(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        tracer = trace.get_tracer(func.__name__)
        with tracer.start_as_current_span(func.__name__):
            start_time = time.time()
            logger.debug(f"Executing {func.__name__} function.")
            result = func(*args, **kwargs)
            end_time = time.time()
            log_execution(func.__name__, end_time - start_time)
            return result

    @wraps(func)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await trace_execution(func, *args, **kwargs)

    @wraps(func)
    def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return trace_execution(func, *args, **kwargs)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
