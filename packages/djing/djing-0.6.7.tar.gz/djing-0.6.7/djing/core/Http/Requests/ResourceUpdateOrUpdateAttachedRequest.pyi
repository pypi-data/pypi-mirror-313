from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources as QueriesResources

class ResourceUpdateOrUpdateAttachedRequest(DjingRequest, QueriesResources):
    request_name: str
