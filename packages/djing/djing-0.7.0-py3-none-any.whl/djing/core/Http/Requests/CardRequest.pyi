from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class CardRequest(DjingRequest):
    def available_cards(self): ...
