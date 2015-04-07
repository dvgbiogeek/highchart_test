from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from api.serializer import PrettyJSONSerializer
from glossary.models import Glossary


class GlossaryResource(ModelResource):
    class Meta:
        queryset = Glossary.objects.all()
        resource_name = 'glossary'
        serializer = PrettyJSONSerializer()
