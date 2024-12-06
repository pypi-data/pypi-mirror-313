from Illuminate.Foundation.Events.Dispatchable import Dispatchable
from _typeshed import Incomplete
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class ServingDjing(Dispatchable):
    request: Incomplete
    def __init__(self, request: DjingRequest) -> None: ...
