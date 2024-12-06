from pyback.rest.errors.base_error import BaseError


class Unauthorized(BaseError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status=401,
            code="UNAUTHORIZED_ERROR",
            title="401: Unauthorized",
        )
