from Illuminate.Collections.Collection import Collection as Collection
from djing.core.Facades.Djing import Djing as Djing
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Menu.MenuGroup import MenuGroup as MenuGroup
from djing.core.Menu.MenuItem import MenuItem as MenuItem
from djing.core.Menu.MenuSection import MenuSection as MenuSection
from djing.core.Tool import Tool as Tool

class ResourceManager(Tool):
    def menu(self, request: DjingRequest): ...
    def grouped_menu(self, grouped_resources, request: DjingRequest): ...
    def ungrouped_menu(self, grouped_resources: Collection, request: DjingRequest): ...
