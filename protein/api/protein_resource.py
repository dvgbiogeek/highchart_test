from tastypie.resources import ModelResource
from api.serializer import PrettyJSONSerializer
from composition.models import Protein


class ProteinResource(ModelResource):
    class Meta:
        queryset = Protein.objects.all()
        resource_name = 'protein'
        serializer = PrettyJSONSerializer()
