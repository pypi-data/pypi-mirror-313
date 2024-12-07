from Illuminate.Contracts.Foundation.Application import Application as Application
from djing.core.Events.DjingServiceProviderRegistered import DjingServiceProviderRegistered as DjingServiceProviderRegistered
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Util import Util as Util
from typing import Any, Callable

class ServeDjing:
    def __init__(self, app: Application) -> None: ...
    def handle(self, request: DjingRequest, next: Callable[[Any], Any]): ...
