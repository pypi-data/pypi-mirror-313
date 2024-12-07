import abc
from abc import abstractmethod

class FilterableField(metaclass=abc.ABCMeta):
    @abstractmethod
    def apply_filter(self, request, query, value): ...
    @abstractmethod
    def resolve_filter(self, request): ...
    @abstractmethod
    def serialize_for_filter(self): ...
