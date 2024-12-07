from Illuminate.Helpers.Util import Util as Util
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Self

class Searchable:
    def searchable(self, searchable: bool = True) -> Self: ...
    def is_searchable(self, request: DjingRequest) -> bool: ...
