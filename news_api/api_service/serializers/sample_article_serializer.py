from .base_serializer import BaseSerializer
from ..models.sample_model import SampleModel


class SampleArticleSerializer(BaseSerializer):
    class Meta:
        model = SampleModel
        exclude = BaseSerializer.Meta.exclude
