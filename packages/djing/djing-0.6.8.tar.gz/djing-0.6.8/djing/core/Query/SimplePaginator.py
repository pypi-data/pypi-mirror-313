from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from Illuminate.Collections.helpers import collect
from djing.core.Http.Requests.DjingRequest import DjingRequest


class SimplePaginator:
    def __init__(self, query: QuerySet, request: DjingRequest):
        self._query = query
        self._request = request
        self._paginator = None
        self._per_page = None
        self._page = None
        self._start_record = None
        self._end_record = None
        self._items = []

    def paginate(self, per_page: int):
        try:
            self._per_page = per_page

            self._page = int(self._request.query_param("page", 1))

            self._paginator = Paginator(self._query.all(), per_page)

            page_obj = self._paginator.page(max(1, self._page))

            self._start_record = (page_obj.number - 1) * per_page + 1

            self._end_record = min(page_obj.number * per_page, self._paginator.count)

            self._items = [field_item for field_item in page_obj]

            return (self, self._paginator.count, True)
        except EmptyPage:
            pass

    def per_page(self):
        return self._per_page

    def page(self):
        return self._page

    def start_record(self):
        return self._start_record

    def end_record(self):
        return self._end_record

    def num_pages(self):
        return self._paginator.num_pages

    def get_collection(self):
        return collect([item for item in self._items])
