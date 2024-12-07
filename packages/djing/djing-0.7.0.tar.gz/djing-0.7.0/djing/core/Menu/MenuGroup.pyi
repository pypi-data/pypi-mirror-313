from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from _typeshed import Incomplete
from djing.core.AuthorizedToSee import AuthorizedToSee as AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable as Collapsable
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Makeable import Makeable as Makeable
from djing.core.Menu.MenuCollection import MenuCollection as MenuCollection

class MenuGroup(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component: str
    name: Incomplete
    def __init__(self, name, items=[]) -> None: ...
    def json_serialize(self) -> dict: ...
