from typing import TYPE_CHECKING, Any, List, Optional, Self


if TYPE_CHECKING:
    from djing.core.Http.Requests.DjingRequest import DjingRequest
    from djing.core.Query.SimplePaginator import SimplePaginator


class QueryBuilder:
    def search(
        self,
        request: "DjingRequest",
        query,
        search: Optional[Any],
        filters: List[Any],
        orderings: List[Any],
    ) -> "SimplePaginator": ...

    def paginate(self, per_page: int) -> Self: ...
