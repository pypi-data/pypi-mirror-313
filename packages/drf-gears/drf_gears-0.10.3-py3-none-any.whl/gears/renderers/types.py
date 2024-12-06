from dataclasses import dataclass
from typing import Union


@dataclass
class Error:
    code: str = None
    location: str = None
    description: str = None
    detail: Union[dict[str, Union[str, int]], None] = None


@dataclass
class Response:
    success: bool
    status_code: int
    pagination: Union[dict, None]
    errors: Union[Error, list]
    data: Union[dict, list, None]
    service_data: Union[dict, list, None]
