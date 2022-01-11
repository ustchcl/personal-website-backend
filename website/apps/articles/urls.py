from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentDestroyAPIView, CommentListCreateAPIView, TagListAPIView, RecommendedArticleAPIView

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^tags/?$', TagListAPIView.as_view()),
    url(r'^recommendArticles/?$', RecommendedArticleAPIView.as_view()),
    url(r'^articles/(?P<article_slug>[-\w]+)/comments/?$', CommentListCreateAPIView.as_view()),
    url(r'^articles/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$', CommentDestroyAPIView.as_view()),
    path('', include(router.urls)),
]