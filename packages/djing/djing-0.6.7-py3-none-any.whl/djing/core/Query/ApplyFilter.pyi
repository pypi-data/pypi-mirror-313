from _typeshed import Incomplete
from django.db.models import QuerySet as QuerySet
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class ApplyFilter:
    filter: Incomplete
    value: Incomplete
    def __init__(self, filter, value) -> None: ...
    def __call__(self, request: DjingRequest, query: QuerySet): ...
