from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import ResourceUpdateOrUpdateAttachedRequest as ResourceUpdateOrUpdateAttachedRequest
from djing.core.Http.Resources.UpdateViewResource import UpdateViewResource as UpdateViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb as Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs as Breadcrumbs
from typing import Any

class ResourceUpdateController:
    def __call__(self, request: ResourceUpdateOrUpdateAttachedRequest) -> Any: ...
