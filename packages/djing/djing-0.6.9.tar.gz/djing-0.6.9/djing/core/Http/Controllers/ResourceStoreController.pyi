from Illuminate.Validation.ValidationResponse import ValidationResponse as ValidationResponse
from djing.core.Http.Requests.CreateResourceRequest import CreateResourceRequest as CreateResourceRequest
from djing.core.Util import Util as Util
from typing import Any

class ResourceStoreController:
    def __call__(self, request: CreateResourceRequest) -> Any: ...
