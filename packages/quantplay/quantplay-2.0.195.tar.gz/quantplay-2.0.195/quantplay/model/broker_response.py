from typing import Any, Literal, TypedDict


class XTSSuccessResponse(TypedDict):
    type: Literal["success", "error"]
    code: str
    description: str
    result: dict[str, Any] | list[dict[str, Any]]


class XTSErrorResponse(TypedDict):
    type: Literal["success", "error"]
    code: str
    description: str


XTSResponse = XTSErrorResponse | XTSErrorResponse
