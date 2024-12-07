from _typeshed import Incomplete
from django.http import HttpRequest as HttpRequest
from djing.core.Djing import Djing as Djing
from djing.core.Exceptions.InvalidLicenseException import InvalidLicenseException as InvalidLicenseException
from djing.djing_application import djing_application as djing_application
from djing.djing_request_adapter import DjingRequestAdapter as DjingRequestAdapter

class DjingMiddleware:
    get_response: Incomplete
    def __init__(self, get_response) -> None: ...
    def __call__(self, request: HttpRequest): ...
