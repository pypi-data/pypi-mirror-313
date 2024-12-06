from django.db.models import base as base
from djing.core.Http.Requests.ResourceUpdateOrUpdateAttachedRequest import ResourceUpdateOrUpdateAttachedRequest as ResourceUpdateOrUpdateAttachedRequest
from djing.core.Http.Resources.Resource import Resource as Resource

class UpdateViewResource(Resource):
    def new_resource_with(self, request: ResourceUpdateOrUpdateAttachedRequest): ...
    def json(self, request: ResourceUpdateOrUpdateAttachedRequest): ...
