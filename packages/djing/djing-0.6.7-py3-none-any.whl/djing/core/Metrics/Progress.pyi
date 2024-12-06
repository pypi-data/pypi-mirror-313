import abc
from Illuminate.Support.builtins import array_merge as array_merge
from _typeshed import Incomplete
from django.db.models import Model, QuerySet as QuerySet
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Metrics.Metric import Metric as Metric
from djing.core.Metrics.ProgressResult import ProgressResult as ProgressResult
from djing.core.Util import Util as Util
from typing import Any, Callable

class Progress(Metric, metaclass=abc.ABCMeta):
    component: str
    def count(self, request: DjingRequest, model: Model | Any, progress: Callable[..., Any], column: Incomplete | None = None, target: Incomplete | None = None): ...
    def sum(self, request: DjingRequest, model: Model | Any, progress: Callable[..., Any], column: Incomplete | None = None, target: Incomplete | None = None): ...
    def aggregate(self, request: DjingRequest, model: Model | Any, function_name, column: str, progress: Callable[..., Any], target: Any): ...
    def results(self, queryset, function_name, column): ...
