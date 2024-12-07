from Illuminate.Collections.Collection import Collection as Collection
from djing.core.Facades.Djing import Djing as Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class DashboardRequest(DjingRequest):
    def available_cards(self, key) -> Collection: ...
