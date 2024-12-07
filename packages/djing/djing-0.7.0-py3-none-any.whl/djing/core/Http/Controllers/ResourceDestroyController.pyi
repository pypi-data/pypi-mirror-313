from Illuminate.Collections.Collection import Collection as Collection
from djing.core.Http.Requests.DeleteResourceRequest import DeleteResourceRequest as DeleteResourceRequest
from typing import Any

class ResourceDestroyController:
    def __call__(self, request: DeleteResourceRequest) -> Any: ...
