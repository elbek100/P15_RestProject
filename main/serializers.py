from rest_framework import serializers

from .models import Todo, Category


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class TodoSerializerForFilter(serializers.Serializer):
    name = serializers.CharField(required=False)
    category_name = serializers.CharField(required=False)
    start = serializers.FloatField(required=False)
    end = serializers.FloatField(required=False)
    color = serializers.CharField(required=False)
    date = serializers.DateTimeField(required=False)


