import abc
from abc import ABC, abstractmethod
from djing.core.AuthorizedToSee import AuthorizedToSee as AuthorizedToSee
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Makeable import Makeable as Makeable

class Tool(ABC, AuthorizedToSee, Makeable, metaclass=abc.ABCMeta):
    def authorize(self, request: DjingRequest): ...
    def boot(self) -> None: ...
    @abstractmethod
    def menu(self, request: DjingRequest): ...
