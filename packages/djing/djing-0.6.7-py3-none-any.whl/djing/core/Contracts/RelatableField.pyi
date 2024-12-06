import abc
from abc import abstractmethod

class RelatableField(metaclass=abc.ABCMeta):
    @abstractmethod
    def relationship_name(self): ...
    @abstractmethod
    def relationship_type(self): ...
