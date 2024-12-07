from Illuminate.Contracts.Foundation.Application import Application as Application
from djing.core.Facades.Djing import Djing as Djing
from djing.core.Providers.DjingServiceProvider import DjingServiceProvider as DjingServiceProvider
from djing.core.Tools.Dashboard import Dashboard as Dashboard
from djing.core.Tools.ResourceManager import ResourceManager as ResourceManager

class BootDjing:
    def handle(self, event) -> None: ...
    def regiter_tools(self) -> None: ...
