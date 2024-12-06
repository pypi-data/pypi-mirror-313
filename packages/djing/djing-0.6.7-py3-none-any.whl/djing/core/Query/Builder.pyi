from django.db.models import QuerySet as QuerySet, base as base
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Query.SimplePaginator import SimplePaginator as SimplePaginator
from djing.core.Resource import Resource as Resource
from djing.core.Util import Util as Util
from typing import Any

class Builder:
    def __init__(self, resource_class: type[Resource]) -> None: ...
    def where_key(self, query: QuerySet, key: int): ...
    def search(self, request: DjingRequest, query: QuerySet, search: Any | None, filters: list[Any] = [], orderings: list[Any] = []): ...
