from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest as ResourceDetailRequest
from djing.core.Http.Resources.DetailViewResource import DetailViewResource as DetailViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb as Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs as Breadcrumbs
from typing import Any

class ResourceDetailController:
    def __call__(self, request: ResourceDetailRequest) -> Any: ...
