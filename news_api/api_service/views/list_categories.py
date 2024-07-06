from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api_service.serializers.categories_serializer import CategoriesResponseSerializer
from api_service.utils.categories import categories


class ListCategoriesView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategoriesResponseSerializer

    @swagger_auto_schema(
        operation_id="list_article_categories",
        operation_description="List all the categories with available news",
        responses={
            200: CategoriesResponseSerializer()
        }
    )
    def get(self, _request):
        data = {
            'results': categories.keys(),
        }

        return Response(data)
