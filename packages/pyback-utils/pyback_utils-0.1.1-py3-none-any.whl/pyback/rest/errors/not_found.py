from pyback.rest.errors.base_error import BaseError


class NotFound(BaseError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status=404,
            code="NOT_FOUND_ERROR",
            title="404: Not Found",
        )
