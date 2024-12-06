from typing import Generic, List, Optional, TypeVar

from pyback.rest.responses.base_response import BaseResponse
from pyback.rest.responses.metadata import Metadata, Pagination

T = TypeVar("T", bound=BaseResponse)


class Response(BaseResponse, Generic[T]):
    data: T | List[T]
    metadata: Metadata = Metadata()
    pagination: Optional[Pagination]
