from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest as ResourceDetailRequest
from djing.core.Http.Resources.DetailViewResource import DetailViewResource as DetailViewResource
from typing import Any

class ResourceShowController:
    def __call__(self, request: ResourceDetailRequest) -> Any: ...
