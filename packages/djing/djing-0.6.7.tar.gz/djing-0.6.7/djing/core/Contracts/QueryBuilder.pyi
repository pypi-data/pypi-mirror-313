from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Query.SimplePaginator import SimplePaginator as SimplePaginator
from typing import Any, Self

class QueryBuilder:
    def search(self, request: DjingRequest, query, search: Any | None, filters: list[Any], orderings: list[Any]) -> SimplePaginator: ...
    def paginate(self, per_page: int) -> Self: ...
