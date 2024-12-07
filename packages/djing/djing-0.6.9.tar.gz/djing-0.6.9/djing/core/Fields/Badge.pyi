import abc
from djing.core.Contracts.FilterableField import FilterableField as FilterableField
from djing.core.Fields.Field import Field as Field
from djing.core.Fields.FieldFilterable import FieldFilterable as FieldFilterable
from djing.core.Fields.Unfillable import Unfillable as Unfillable

class Badge(Field, FieldFilterable, FilterableField, Unfillable, metaclass=abc.ABCMeta): ...
