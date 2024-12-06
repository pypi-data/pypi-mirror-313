from pyback.rest.errors.base_error import BaseError


class BadRequest(BaseError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status=400,
            code="BAD_REQUEST_ERROR",
            title="400: Bad Request",
        )
