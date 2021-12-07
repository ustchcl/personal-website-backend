from django.conf.urls import url
from .views import ProfileRetrieveUpdateAPIView

urlpatterns = [
    url(r'^profiles/(?P<username>\w+)/?$', ProfileRetrieveUpdateAPIView.as_view())
]