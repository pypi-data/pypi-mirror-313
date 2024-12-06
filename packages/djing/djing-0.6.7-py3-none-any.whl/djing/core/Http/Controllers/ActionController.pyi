from Illuminate.Validation.ValidationResponse import ValidationResponse as ValidationResponse
from djing.core.Http.Requests.ActionRequest import ActionRequest as ActionRequest
from djing.core.Resource import Resource as Resource
from typing import Any

class ActionController:
    def index(self, request: ActionRequest) -> Any: ...
    def store(self, request: ActionRequest): ...
