from djing.core.Http.Requests.ResourceCreateOrAttachRequest import ResourceCreateOrAttachRequest as ResourceCreateOrAttachRequest
from djing.core.Menu.Breadcrumb import Breadcrumb as Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs as Breadcrumbs
from typing import Any

class ResourceReplicateController:
    def __call__(self, request: ResourceCreateOrAttachRequest) -> Any: ...
