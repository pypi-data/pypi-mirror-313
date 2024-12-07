from Illuminate.Collections.Collection import Collection as Collection
from djing.core.Filters.FilterDecoder import FilterDecoder as FilterDecoder
from djing.core.Resource import Resource as Resource

class DecodesFilters:
    def filters(self) -> Collection: ...
    def available_filters(self): ...
