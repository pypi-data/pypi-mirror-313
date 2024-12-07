import abc
from djing.core.Contracts.ListableField import ListableField as ListableField
from djing.core.Contracts.RelatableField import RelatableField as RelatableField
from djing.core.Fields.Field import Field as Field

class BelongsToMany(Field, ListableField, RelatableField, metaclass=abc.ABCMeta):
    component: str
    def json_serialize(self): ...
