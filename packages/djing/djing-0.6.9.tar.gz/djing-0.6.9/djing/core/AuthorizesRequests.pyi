from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any, Callable

class AuthorizesRequests:
    @classmethod
    def auth(cls, callback: Callable[[Any], Any]): ...
    @classmethod
    def check(cls, request: DjingRequest) -> bool: ...
