from pyback.rest.errors.base_error import BaseError


class Forbidden(BaseError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status=403,
            code="FORBIDDEN_ERROR",
            title="403: Forbidden",
        )
