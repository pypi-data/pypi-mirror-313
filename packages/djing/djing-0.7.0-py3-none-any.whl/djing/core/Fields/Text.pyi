from djing.core.Contracts.FilterableField import FilterableField as FilterableField
from djing.core.Fields.AsHtml import AsHtml as AsHtml
from djing.core.Fields.Copyable import Copyable as Copyable
from djing.core.Fields.Field import Field as Field
from djing.core.Fields.FieldFilterable import FieldFilterable as FieldFilterable
from djing.core.Fields.Filters.TextFilter import TextFilter as TextFilter
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class Text(Field, AsHtml, Copyable, FieldFilterable, FilterableField):
    component: str
    def make_filter(self, request: DjingRequest): ...
    def serialize_for_filter(self): ...
    def json_serialize(self): ...
