from rest_framework import serializers

from .models import Article, Comment, Tag
from .relations import TagRelationField


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=True)
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False)

    tagList = TagRelationField(many=True, required=False, source='tags')
    cover = serializers.FileField(max_length=255)
    markdown = serializers.FileField(max_length=255)

    # Django REST Framework makes it possible to create a read-only field that
    # gets it's value by calling a function. In this case, the client expects
    # `created_at` to be called `createdAt` and `updated_at` to be `updatedAt`.
    # `serializers.SerializerMethodField` is a good way to avoid having the
    # requirements of the client leak into our API.
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')


    class Meta:
        model = Article
        fields = (
            'author',
            'body',

        )

    def create(self, validated_data):
        tags = validated_data 

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def get_created_at(self, instance):
        return instance.created_at.isoformat()