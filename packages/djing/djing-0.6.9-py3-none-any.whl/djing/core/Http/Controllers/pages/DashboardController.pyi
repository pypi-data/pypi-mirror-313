from djing.core.Facades.Djing import Djing as Djing
from djing.core.Http.Requests.DashboardRequest import DashboardRequest as DashboardRequest
from djing.core.Http.Resources.DashboardViewResource import DashboardViewResource as DashboardViewResource
from djing.core.Menu.Breadcrumb import Breadcrumb as Breadcrumb
from djing.core.Menu.Breadcrumbs import Breadcrumbs as Breadcrumbs
from typing import Any

class DashboardController:
    def __call__(self, request: DashboardRequest) -> Any: ...
