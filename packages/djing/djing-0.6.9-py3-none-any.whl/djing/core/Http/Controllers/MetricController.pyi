from djing.core.Http.Requests.MetricRequest import MetricRequest as MetricRequest
from typing import Any

class MetricController:
    def show(self, request: MetricRequest) -> Any: ...
