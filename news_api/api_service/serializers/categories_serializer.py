from rest_framework import serializers


class CategoriesResponseSerializer(serializers.Serializer):
    results = serializers.ListField(child=serializers.CharField())
