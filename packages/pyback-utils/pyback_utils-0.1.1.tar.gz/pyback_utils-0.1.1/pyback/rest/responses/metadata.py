from typing import Any, Dict, Optional

from opentelemetry import trace

from pyback.rest.responses.base_response import BaseResponse


def get_trace_id() -> str:
    span = trace.get_current_span()
    trace_id = span.get_span_context().trace_id
    return str(format(trace_id, "032x"))


class Metadata(BaseResponse):
    trace_id: str = get_trace_id()
    service_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
