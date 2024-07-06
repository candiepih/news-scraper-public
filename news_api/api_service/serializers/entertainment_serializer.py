from .base_serializer import BaseSerializer
from api_service.models import Entertainment


class EntertainmentSerializer(BaseSerializer):
    class Meta:
        model = Entertainment
        exclude = BaseSerializer.Meta.exclude
