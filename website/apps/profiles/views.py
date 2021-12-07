from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Create your views here.

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer

class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permissions = (AllowAny, )
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def update(self, request, username):
        try:
            profile = self.queryset.get(user__username=username)            
        except Profile.DoesNotExist:
            raise NotFound('Profile does not exist')

        bio = request.data.get('bio', profile.bio)
        image = request.data.get('image', profile.image)
        serializer_data = {
            'bio': bio,
            'image': image
        }
        print (serializer_data)
        serializer = self.serializer_class(profile, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, username):
        print("username: ", username)
        try:
            print(self.serializer_class(self.get_queryset(), many=True).data)
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('Profile does not exist')
        
        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)