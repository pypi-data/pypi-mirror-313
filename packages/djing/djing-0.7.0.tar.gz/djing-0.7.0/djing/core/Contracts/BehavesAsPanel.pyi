import abc
from abc import abstractmethod

class BehavesAsPanel(metaclass=abc.ABCMeta):
    @abstractmethod
    def as_panel(self): ...
