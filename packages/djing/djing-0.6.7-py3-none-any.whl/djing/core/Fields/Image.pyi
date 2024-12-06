from _typeshed import Incomplete
from djing.core.Fields.File import File as File
from djing.core.Fields.PresentsImages import PresentsImages as PresentsImages

class Image(File, PresentsImages):
    ASPECT_AUTO: str
    ASPECT_SQUARE: str
    def __init__(self, name, attribute: Incomplete | None = None, disk: Incomplete | None = None, storage_callback: Incomplete | None = None) -> None: ...
    def json_serialize(self): ...
