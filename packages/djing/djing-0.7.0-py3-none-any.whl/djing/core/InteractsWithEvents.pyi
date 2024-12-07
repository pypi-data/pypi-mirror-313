from djing.core.Events.DjingServiceProviderRegistered import DjingServiceProviderRegistered as DjingServiceProviderRegistered
from djing.core.Events.ServingDjing import ServingDjing as ServingDjing
from typing import Any, Callable

class InteractsWithEvents:
    @classmethod
    def booted(cls, callback: Callable[[Any], Any]): ...
    @classmethod
    def serving(cls, callback: Callable[[Any], Any]): ...
