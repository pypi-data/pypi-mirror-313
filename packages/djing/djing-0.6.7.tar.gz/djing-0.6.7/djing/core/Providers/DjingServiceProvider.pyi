from Illuminate.Contracts.Foundation.Application import Application as Application
from Illuminate.Support.ServiceProvider import ServiceProvider
from _typeshed import Incomplete
from djing.core.Console.ActionCommand import ActionCommand as ActionCommand
from djing.core.Console.BaseResourceCommand import BaseResourceCommand as BaseResourceCommand
from djing.core.Console.DashboardCommand import DashboardCommand as DashboardCommand
from djing.core.Console.DjingServiceProviderCommand import DjingServiceProviderCommand as DjingServiceProviderCommand
from djing.core.Console.FilterCommand import FilterCommand as FilterCommand
from djing.core.Console.InstallCommand import InstallCommand as InstallCommand
from djing.core.Console.ProgressMetricCommand import ProgressMetricCommand as ProgressMetricCommand
from djing.core.Console.PublishCommand import PublishCommand as PublishCommand
from djing.core.Console.ResourceCommand import ResourceCommand as ResourceCommand
from djing.core.Console.ValueMetricCommand import ValueMetricCommand as ValueMetricCommand

class DjingServiceProvider(ServiceProvider):
    app: Incomplete
    def __init__(self, app: Application) -> None: ...
    def register(self) -> None: ...
    def boot(self) -> None: ...
