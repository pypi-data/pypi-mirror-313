from _typeshed import Incomplete
from django.db.models import base as base
from djing.core.Http.Requests.ResourceCreateOrAttachRequest import ResourceCreateOrAttachRequest as ResourceCreateOrAttachRequest
from djing.core.Http.Resources.CreateViewResource import CreateViewResource as CreateViewResource

class ReplicateViewResource(CreateViewResource):
    from_resource_id: Incomplete
    def __init__(self, from_resource_id) -> None: ...
    def new_resource_with(self, request: ResourceCreateOrAttachRequest): ...
