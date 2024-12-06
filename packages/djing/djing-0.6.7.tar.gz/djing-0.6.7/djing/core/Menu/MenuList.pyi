from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from djing.core.AuthorizedToSee import AuthorizedToSee as AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable as Collapsable
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Makeable import Makeable as Makeable
from djing.core.Menu.MenuCollection import MenuCollection as MenuCollection
from typing import Self

class MenuList(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component: str
    def __init__(self, items) -> None: ...
    def items(self, items=[]) -> Self: ...
    def json_serialize(self) -> dict: ...
