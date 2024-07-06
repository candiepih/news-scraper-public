from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class BaseSerializer(ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        exclude = ('digest', 'updatedAt')
