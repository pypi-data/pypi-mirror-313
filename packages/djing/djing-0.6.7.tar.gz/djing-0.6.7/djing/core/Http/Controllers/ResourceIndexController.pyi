from djing.core.Http.Requests.ResourceIndexRequest import ResourceIndexRequest as ResourceIndexRequest
from djing.core.Http.Resources.IndexViewResource import IndexViewResource as IndexViewResource
from typing import Any

class ResourceIndexController:
    def __call__(self, request: ResourceIndexRequest) -> Any: ...
