from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any

class FilterController:
    def __call__(self, request: DjingRequest) -> Any: ...
