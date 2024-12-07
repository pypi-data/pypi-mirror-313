from _typeshed import Incomplete
from djing.core.Fields.Text import Text as Text

class Hidden(Text):
    component: str
    def __init__(self, name, attribute: Incomplete | None = None, resolve_callback: Incomplete | None = None) -> None: ...
