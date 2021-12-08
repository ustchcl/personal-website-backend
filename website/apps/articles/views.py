from rest_framework import serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView

from .models import Article
from .serializers import ArticleSerializer
# Create your views here.


class ArticleListCreateAPIView(ListCreateAPIView):
    queryset= Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    


