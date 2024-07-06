from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from api_service.models.sample_model import SampleModel
from api_service.serializers.sample_article_serializer import SampleArticleSerializer
from api_service.utils.categories import categories
from django.conf import settings


class ListArticlesView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SampleArticleSerializer
    model = SampleModel

    def get_queryset(self):
        kwargs = self.request.parser_context.get('kwargs')
        category_name = kwargs.get('category_name')

        category = categories.get(category_name, None)

        if not category:
            self.serializer_class = SampleArticleSerializer
            return SampleModel.objects.none()

        # set serializer class
        self.serializer_class = category.get('serializer_class')

        # set queryset
        model = category.get('model')
        self.model = model

        queryset = model.objects.all()

        return queryset

    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    @swagger_auto_schema(
        operation_id="list_articles",
        operation_description="List all the news articles available in a certain category",
        responses={
            200: SampleArticleSerializer()
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
