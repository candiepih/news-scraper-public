from .base_serializer import BaseSerializer
from api_service.models import Sports


class SportsSerializer(BaseSerializer):
    class Meta:
        model = Sports
        exclude = BaseSerializer.Meta.exclude
