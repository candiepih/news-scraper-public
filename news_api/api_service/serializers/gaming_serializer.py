from .base_serializer import BaseSerializer
from api_service.models import VideoGames


class VideoGamesSerializer(BaseSerializer):
    class Meta:
        model = VideoGames
        exclude = BaseSerializer.Meta.exclude
