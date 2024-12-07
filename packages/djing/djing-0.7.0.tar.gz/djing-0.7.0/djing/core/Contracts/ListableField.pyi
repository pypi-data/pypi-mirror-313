import abc
from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel as BehavesAsPanel

class ListableField(BehavesAsPanel, metaclass=abc.ABCMeta): ...
