import abc
from abc import abstractmethod

class Storable(metaclass=abc.ABCMeta):
    @abstractmethod
    def get_storage_disk(self): ...
