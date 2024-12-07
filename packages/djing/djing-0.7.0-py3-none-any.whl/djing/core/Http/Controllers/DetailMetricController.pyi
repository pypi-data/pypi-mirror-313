from djing.core.Http.Requests.MetricRequest import MetricRequest as MetricRequest
from typing import Any

class DetailMetricController:
    def __call__(self, request: MetricRequest) -> Any: ...
