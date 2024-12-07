from Illuminate.Support.builtins import array_merge
from djing.core.Fields.Field import Field
from djing.core.Http.Requests.DjingRequest import DjingRequest
from django.contrib.auth.hashers import make_password


class Password(Field):
    component = "password-field"

    def fill_attribute_from_request(
        self, request: DjingRequest, request_attribute, model, attribute
    ):
        if request_attribute in request.all():
            value = request.all().get(request_attribute)

            if value is not None:
                setattr(model, attribute, make_password(value))

    def json_serialize(self):
        return array_merge(
            super().json_serialize(),
            {
                "value": "",
            },
        )
