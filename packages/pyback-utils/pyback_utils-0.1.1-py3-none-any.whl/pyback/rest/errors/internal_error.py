from pyback.rest.errors.base_error import BaseError


class InternalError(BaseError):
    def __init__(self):
        super().__init__(
            message="An unexpected error occurred.",
            status=500,
            code="INTERNAL_ERROR",
            title="500: Internal Error",
        )
