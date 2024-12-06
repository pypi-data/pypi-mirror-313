from Illuminate.Routing.Router import Router as Router
from djing.core.Facades.Djing import Djing as Djing
from djing.core.Http.Controllers.HomeController import HomeController as HomeController
from djing.core.Http.Controllers.LoginController import LoginController as LoginController
from djing.core.Http.Controllers.pages.DashboardController import DashboardController as DashboardController
from djing.core.Http.Controllers.pages.ResourceCreateController import ResourceCreateController as ResourceCreateController
from djing.core.Http.Controllers.pages.ResourceDetailController import ResourceDetailController as ResourceDetailController
from djing.core.Http.Controllers.pages.ResourceIndexController import ResourceIndexController as ResourceIndexController
from djing.core.Http.Controllers.pages.ResourceReplicateController import ResourceReplicateController as ResourceReplicateController
from djing.core.Http.Controllers.pages.ResourceUpdateController import ResourceUpdateController as ResourceUpdateController
from typing import Self

class PendingRouteRegistration:
    def __init__(self) -> None: ...
    def with_authentication_routes(self) -> Self: ...
    def register(self) -> None: ...
