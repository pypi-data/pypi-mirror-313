from django.db.models import base as base
from djing.core.Fields.FieldCollection import FieldCollection as FieldCollection
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any, Callable

class FillsFields:
    @classmethod
    def fill(cls, request: DjingRequest, model: base.Model) -> tuple[base.Model, Callable[..., Any]]: ...
    @classmethod
    def fill_for_update(cls, request: DjingRequest, model: base.Model): ...
