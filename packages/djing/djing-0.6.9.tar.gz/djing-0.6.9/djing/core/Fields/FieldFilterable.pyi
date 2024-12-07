import abc
from django.db.models import QuerySet as QuerySet
from djing.core.Fields.Filterable import Filterable as Filterable
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class FieldFilterable(Filterable, metaclass=abc.ABCMeta):
    def serialize_for_filter(self): ...
