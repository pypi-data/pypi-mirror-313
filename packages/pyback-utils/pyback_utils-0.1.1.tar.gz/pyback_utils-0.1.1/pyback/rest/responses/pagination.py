from pyback.rest.responses.base_response import BaseResponse


class Pagination(BaseResponse):
    total: int
    page: int
    per_page: int
    pages: int
