from djing.core.Http.Requests.CardRequest import CardRequest as CardRequest
from typing import Any

class CardController:
    def __call__(self, request: CardRequest) -> Any: ...
