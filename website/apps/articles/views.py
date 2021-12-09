from django.db.models.query import QuerySet
from rest_framework import serializers, viewsets, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin
)

from website.apps.articles.renders import ArticleJSONRenderer

from .models import Article
from .serializers import ArticleSerializer
# Create your views here.


class ArticleListCreateAPIView(ListCreateAPIView):
    queryset= Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    


class AtricleViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):

    lookup_field = "slug"
    query_set = Article.objects.all()
    permission_classes = (AllowAny,)
    renderer_classes = ArticleJSONRenderer
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)
        return queryset

    def create(self, request):
        serializer_data = request.data.get('article')
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
            serializer_instance = self.query_set.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("'An article with this slug does not exist.")

        serializer = self.serializer_class(data=serializer_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    



