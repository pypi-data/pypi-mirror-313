from _typeshed import Incomplete
from djing.core.Contracts.FilterableField import FilterableField as FilterableField
from djing.core.Fields.Field import Field as Field
from djing.core.Fields.FieldFilterable import FieldFilterable as FieldFilterable
from djing.core.Fields.Filters.TextFilter import TextFilter as TextFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class Textarea(Field, FieldFilterable, FilterableField):
    component: str
    rows: int
    def make_filter(self, request: DjingRequest): ...
    def resolve_for_display(self, resource, attribute: Incomplete | None = None): ...
    def json_serialize(self): ...
