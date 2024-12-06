from pyback.rest.responses.base_response import BaseResponse


class Error(BaseResponse):
    status: int
    code: str
    title: str
    detail: str
