from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ArticleListCreateAPIView

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'articles', ArticleViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('', include(router.urls)),
    url(r'^articles/$',ArticleListCreateAPIView.as_view())
]