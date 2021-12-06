from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Create your views here.

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer

class ProfileRetrieveAPIView(RetrieveAPIView):
    permissions = (AllowAny)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('Profile does not exist')
        
        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)