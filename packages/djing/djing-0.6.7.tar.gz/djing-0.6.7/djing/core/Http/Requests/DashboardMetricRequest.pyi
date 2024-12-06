from djing.core.Djing import Djing as Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources as QueriesResources
from djing.core.Metrics.Metric import Metric as Metric

class DashboardMetricRequest(DjingRequest, QueriesResources):
    request_name: str
    def metric(self): ...
    def available_metrics(self): ...
