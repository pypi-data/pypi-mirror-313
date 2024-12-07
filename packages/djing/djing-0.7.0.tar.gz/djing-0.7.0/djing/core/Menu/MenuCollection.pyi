from Illuminate.Collections.Collection import Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Self

class MenuCollection(Collection):
    def authorize(self, request: DjingRequest) -> Self: ...
    def without_empty_items(self): ...
