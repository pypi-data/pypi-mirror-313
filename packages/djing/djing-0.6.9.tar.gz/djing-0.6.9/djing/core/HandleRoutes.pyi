import abc
from abc import abstractmethod

class HandleRoutes(metaclass=abc.ABCMeta):
    @classmethod
    @abstractmethod
    def path(cls) -> str: ...
    @classmethod
    def url(cls, url: str) -> str: ...
