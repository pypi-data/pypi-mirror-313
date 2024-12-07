from djing.core.Contracts.QueryBuilder import QueryBuilder as QueryBuilder
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources as QueriesResources
from djing.core.Query.SimplePaginator import SimplePaginator as SimplePaginator

class ResourceIndexRequest(DjingRequest, QueriesResources):
    request_name: str
    def search_index(self) -> tuple[SimplePaginator, int, bool]: ...
    def per_page(self) -> int: ...
