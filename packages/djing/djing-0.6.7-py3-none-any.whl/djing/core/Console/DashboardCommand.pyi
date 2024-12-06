from Illuminate.Foundation.Console.GeneratorCommand import GeneratorCommand
from pathlib import Path

class DashboardCommand(GeneratorCommand):
    name: str
    description: str
    type: str
    def get_stub(self): ...
    def get_stub_vars(self): ...
    def get_default_namespace(self, root_namespace: Path): ...
