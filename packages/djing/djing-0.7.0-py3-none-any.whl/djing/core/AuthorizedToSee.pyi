from _typeshed import Incomplete
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class AuthorizedToSee:
    see_callback: Incomplete
    def authorized_to_see(self, request: DjingRequest): ...
    def can_see(self, callback): ...
