from djing.core.Facades.Djing import Djing as Djing
from djing.core.HasMenu import HasMenu as HasMenu
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Menu.MenuSection import MenuSection as MenuSection
from djing.core.Tool import Tool as Tool

class Dashboard(Tool, HasMenu):
    def menu(self, request: DjingRequest): ...
