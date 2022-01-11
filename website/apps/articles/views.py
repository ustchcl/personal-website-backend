from django.db.models.query import QuerySet
from rest_framework import serializers, viewsets, mixins, status
from rest_framework import decorators
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import DestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin
)

from website.apps.articles.renders import ArticleJSONRenderer, CommentJSONRender

from .models import Article, Comment, Tag
from .serializers import ArticleSerializer, CommentSerializer, TagSerializer
# Create your views here.


class ArticleListCreateAPIView(ListCreateAPIView):
    queryset= Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    


class ArticleViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):

    lookup_field = "slug"
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)
        return queryset

    def create(self, request):
        tags = request.data.get("tagList", '').split(',')
        print('tags', tags)
        serializer_data = {
            'cover': request.data.get('cover', None),
            'title': request.data.get('title', None),
            'markdown_path': request.data.get('markdown_path', None),
            'description': request.data.get('description', None),
            'recommended': request.data.get('recommended', False),
            'tagList': [ tag for tag in tags if len(tag) > 0 ]
        }
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        try:
            serializer_instance = self.get_queryset().get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist.")

        serializer = self.serializer_class(serializer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, slug):
        try:
            serializer_instance = self.get_queryset().get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist.")
        serializer_instance.delete()
        return Response({"message": "ok"}, status=status.HTTP_204_NO_CONTENT)
     
    def update(self, request, slug):
        try:
            serializer_instance = self.get_queryset().get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist.")
        
        tags = request.data.get("tagList", '').split(',')
        serializer_data = {
            'tagList': [ tag for tag in tags if len(tag) > 0 ]
        }

        cover = request.data.get('cover', None)
        if cover is not None:
            serializer_data['cover'] = cover

        title = request.data.get('title', None)
        if title is not None:
            serializer_data['title'] = title

        markdown_path = request.data.get('markdown_path', None)
        if markdown_path is not None:
            serializer_data['markdown_path'] = markdown_path

        description = request.data.get('description', None)
        if description is not None:
            serializer_data['description'] = description

        recommended = request.data.get('recommended', None)
        if recommended is not None:
            serializer_data['recommended'] = recommended
        
        serializer = self.serializer_class(serializer_instance, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)



class RecommendedArticleAPIView(ListAPIView):
    queryset = Article.objects.all().filter(recommended=True)
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)


class CommentListCreateAPIView(ListCreateAPIView):
    lookup_field = "article__slug"
    lookup_url_kwarg = "article__slug"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer
    renderer_classes = CommentJSONRender
    
    queryset = Comment.objects.select_related(
        "author", "author__user", "article"
    )

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)
    
    def create(self, request, article_slug=None):
        data = request.data.get("article", {})
        context = {'author': request.user.profile}
        
        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound("An article with this slug does not exist.")
        
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentDestroyAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_pk'
    
    def delete(self, request, article_slug=None, comment_pk=None):
        try:
            comment = self.queryset.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound("The comment with this pk does not exist.")
        
        comment.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class TagListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    
    def list(self, request):
        tags = self.get_queryset()
        serializer = self.serializer_class(tags, many=True)
        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)