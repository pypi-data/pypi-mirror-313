from djing.core.Filters.Filter import Filter as Filter
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class BooleanFilter(Filter):
    component: str
    def default(self): ...
