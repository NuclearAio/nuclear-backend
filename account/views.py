from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST
)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    try:
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        password = data.get('password')
        user_object = User(
            username=username,
            first_name=first_name,
            is_staff=True
        )
        user_object.set_password(password)
        user_object.save()
        return Response(status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        # token['is_staff'] = user.is_staff
        return token

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


@api_view(['GET'])
def get_user_profile(request):
    try:
        pass
    except Exception as error:
        pass