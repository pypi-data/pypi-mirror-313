import abc
from abc import abstractmethod
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class HasMenu(metaclass=abc.ABCMeta):
    @abstractmethod
    def menu(self, request: DjingRequest): ...
