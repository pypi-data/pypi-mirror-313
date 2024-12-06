import abc
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel as BehavesAsPanel
from djing.core.Contracts.RelatableField import RelatableField as RelatableField
from djing.core.Fields.Field import Field as Field

class HasOne(Field, BehavesAsPanel, RelatableField, metaclass=abc.ABCMeta):
    component: str
    def json_serialize(self): ...
