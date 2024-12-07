from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources as QueriesResources

class UpdateResourceRequest(DjingRequest, QueriesResources):
    request_name: str
    def is_update_or_update_attached_request(self) -> bool: ...
