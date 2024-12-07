from _typeshed import Incomplete
from djing.core.Fields.Image import Image as Image

class Avatar(Image):
    def __init__(self, name, attribute: Incomplete | None = None, disk: Incomplete | None = None, storage_callback: Incomplete | None = None) -> None: ...
    @classmethod
    def gravatar(cls, name: str = 'Avatar', attribute: str = 'email'): ...
