from djing.core.Contracts.Downloadable import Downloadable as Downloadable
from djing.core.Fields.DeleteField import DeleteField as DeleteField
from djing.core.Http.Requests.ResourceDestroyRequest import ResourceDestroyRequest as ResourceDestroyRequest
from typing import Any

class FieldDestroyController:
    def __call__(self, request: ResourceDestroyRequest) -> Any: ...
