from djing.core.Filters.Filter import Filter as Filter
from typing import Self

class DateFilter(Filter):
    component: str
    def first_day_of_week(self, day) -> Self: ...
