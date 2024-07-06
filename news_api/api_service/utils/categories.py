from api_service.models import *
from api_service.serializers import *

categories = {
    'entertainment': {
        'serializer_class': EntertainmentSerializer,
        'model': Entertainment
    },
    'global_news': {
        'serializer_class': GlobalNewsSerializer,
        'model': GlobalNews
    },
    'technology': {
        'serializer_class': TechnologySerializer,
        'model': Technology
    },
    'sports': {
        'serializer_class': SportsSerializer,
        'model': Sports
    },
    'video_games': {
        'serializer_class': VideoGamesSerializer,
        'model': VideoGames
    },
}
