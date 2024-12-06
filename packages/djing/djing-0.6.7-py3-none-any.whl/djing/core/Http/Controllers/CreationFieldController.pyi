from djing.core.Http.Requests.ResourceCreateOrAttachRequest import ResourceCreateOrAttachRequest as ResourceCreateOrAttachRequest
from djing.core.Http.Resources.CreateViewResource import CreateViewResource as CreateViewResource
from djing.core.Http.Resources.ReplicateViewResource import ReplicateViewResource as ReplicateViewResource
from typing import Any

class CreationFieldController:
    def __call__(self, request: ResourceCreateOrAttachRequest) -> Any: ...
