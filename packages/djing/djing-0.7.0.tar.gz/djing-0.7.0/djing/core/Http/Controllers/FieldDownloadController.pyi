from djing.core.Http.Requests.ResourceDownloadRequest import ResourceDownloadRequest as ResourceDownloadRequest
from typing import Any

class FieldDownloadController:
    def __call__(self, request: ResourceDownloadRequest) -> Any: ...
