from typing import Type

from opentelemetry import trace
from starlette.requests import Request
from starlette.responses import JSONResponse

from pyback.logger import logger
from pyback.rest.errors import InternalError
from pyback.rest.errors.base_error import BaseError
from pyback.rest.responses.error import Error


async def _is_not_a_custom_exc(exc: Type[BaseError] | Type[Exception]) -> bool:
    if issubclass(type(exc), BaseError):
        return False
    return True


async def base_error_exception_handler(
    request: Request, exc: Type[BaseError] | Exception
):
    if await _is_not_a_custom_exc(exc):
        exc = InternalError()

    span = trace.get_current_span()
    span.record_exception(exc)
    span.set_status(trace.StatusCode.ERROR, exc.message)
    logger.error(f"{exc.code}: {exc.message}")

    error = Error(
        status=exc.status,
        code=exc.code,
        title=exc.title,
        detail=exc.message,
    )

    content = error.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)

    return JSONResponse(status_code=error.status, content=content)
