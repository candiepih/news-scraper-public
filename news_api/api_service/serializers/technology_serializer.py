from .base_serializer import BaseSerializer
from api_service.models import Technology


class TechnologySerializer(BaseSerializer):
    class Meta:
        model = Technology
        exclude = BaseSerializer.Meta.exclude
