from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class CreateResourceRequest(DjingRequest):
    request_name: str
    def is_create_or_attach_request(self) -> bool: ...
