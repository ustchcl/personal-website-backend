from rest_framework import serializers

from website.apps.profiles.serializers import ProfileSerializer

from .models import Article, Comment, Tag
from .relations import TagRelationField



class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False)

    tagList = TagRelationField(many=True, required=False, source='tags')
    cover = serializers.FileField(max_length=255)
    markdown_path = serializers.CharField(required=True)

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
            'slug',
            'title',
            'description',
            'tagList',
            'cover',
            'markdown_path',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tag', [])
        article = Article.objects.create(**validated_data)
        
        print('tags: ', tags)
        
        for tag in tags:
            article.tags.add(tag)
        
        return article

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def get_created_at(self, instance):
        return instance.created_at.isoformat()
    
    
class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        article = self.context['article']
        author = self.context['author']

        return Comment.objects.create(
            author=author, article=article, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, obj):
        return obj.tag
