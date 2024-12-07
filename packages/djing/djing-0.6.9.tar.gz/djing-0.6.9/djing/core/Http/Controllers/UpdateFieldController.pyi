from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import ResourceUpdateOrUpdateAttachedRequest as ResourceUpdateOrUpdateAttachedRequest
from djing.core.Http.Resources.UpdateViewResource import UpdateViewResource as UpdateViewResource
from typing import Any

class UpdateFieldController:
    def __call__(self, request: ResourceUpdateOrUpdateAttachedRequest) -> Any: ...
