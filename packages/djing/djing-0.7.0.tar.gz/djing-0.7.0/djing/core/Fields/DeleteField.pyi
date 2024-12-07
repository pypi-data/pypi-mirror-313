from django.db.models.base import Model as Model
from djing.core.Contracts.Storable import Storable as Storable
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any

class DeleteField:
    @classmethod
    def for_request(cls, request: DjingRequest, field: Any, model: Model): ...
