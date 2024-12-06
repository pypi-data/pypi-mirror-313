__all__ = [
    "base_error_exception_handler",
]

from typing import Type

from starlette.applications import Starlette

from pyback.rest.errors.base_error import BaseError

from .base_error_handler import base_error_exception_handler


def add_handlers(app: Type[Starlette]) -> None:
    app.add_exception_handler(BaseError, base_error_exception_handler)
    app.add_exception_handler(Exception, base_error_exception_handler)
