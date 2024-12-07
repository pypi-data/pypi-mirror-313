from Illuminate.Contracts.Foundation.Application import Application as Application
from djing.core.Facades.Djing import Djing as Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any, Callable

class HandleInertiaRequests:
    def __init__(self, app: Application) -> None: ...
    def handle(self, request: DjingRequest, next: Callable[[Any], Any]): ...
