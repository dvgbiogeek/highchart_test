from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from api.serializer import PrettyJSONSerializer
from composition.models import Protein


class ProteinResource(ModelResource):
    class Meta:
        queryset = Protein.objects.all()
        resource_name = 'protein'
        serializer = PrettyJSONSerializer()
        authorization = Authorization()
        always_return_data = True
