from .base_serializer import BaseSerializer
from api_service.models import GlobalNews


class GlobalNewsSerializer(BaseSerializer):
    class Meta:
        model = GlobalNews
        exclude = BaseSerializer.Meta.exclude
