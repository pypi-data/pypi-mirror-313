from Illuminate.Contracts.Foundation.Application import Application as Application
from Illuminate.Support.ServiceProvider import ServiceProvider
from _typeshed import Incomplete
from djing.core.Contracts.QueryBuilder import QueryBuilder as QueryBuilder
from djing.core.Djing import Djing as Djing
from djing.core.Http.Middlewares.ServeDjing import ServeDjing as ServeDjing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Listeners.BootDjing import BootDjing as BootDjing
from djing.core.Providers.DjingServiceProvider import DjingServiceProvider as DjingServiceProvider
from djing.core.Query.Builder import Builder as Builder
from djing.core.Util import Util as Util

class DjingCoreServiceProvider(ServiceProvider):
    app: Incomplete
    def __init__(self, app: Application) -> None: ...
    def register(self): ...
    def boot(self) -> None: ...
