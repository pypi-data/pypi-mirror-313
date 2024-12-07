from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources as QueriesResources
from djing.core.Resource import Resource as Resource

class DeletionRequest(QueriesResources, DjingRequest):
    def chunk_with_authorization(self, count, callback, auth_callback): ...
    def to_selected_resource_query(self): ...
