from djing.core.Http.Requests.DashboardRequest import DashboardRequest as DashboardRequest
from djing.core.Http.Resources.DashboardViewResource import DashboardViewResource as DashboardViewResource
from typing import Any

class DashboardController:
    def __call__(self, request: DashboardRequest) -> Any: ...
