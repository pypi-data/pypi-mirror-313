from Illuminate.Contracts.Foundation.Application import Application as Application
from djing.core.Events.ServingDjing import ServingDjing as ServingDjing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any, Callable

class DispatchServingDjingEvent:
    def __init__(self, app: Application) -> None: ...
    def handle(self, request: DjingRequest, next: Callable[[Any], Any]): ...
