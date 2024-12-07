from djing.core.Fields.Field import Field as Field
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest

class Password(Field):
    component: str
    def fill_attribute_from_request(self, request: DjingRequest, request_attribute, model, attribute): ...
    def json_serialize(self): ...
