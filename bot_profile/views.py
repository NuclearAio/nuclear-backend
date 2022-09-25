from os import stat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT,
    HTTP_206_PARTIAL_CONTENT,
)

from .models import BotProfile
from .serializers import BotProfileSerializer

@api_view(['GET'])
def get_bot_profiles(request):
    try: 
        user = request.user
        paginator = PageNumberPagination()
        paginator.page_size = 1
        bot_profile_objects  = BotProfile.objects.filter(user=user)
        paginated_objects = paginator.paginate_queryset(bot_profile_objects, request)
        serializer = BotProfileSerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_bot_profile(request):
    try:
        user = request.user
        title = request.data.get('title')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        address_1 = request.data.get('address_1')
        address_2 = request.data.get('address_2')
        phone_number = request.data.get('phone_number')
        country = request.data.get('country')
        state = request.data.get('state')
        city = request.data.get('city')
        zip = request.data.get('zip')

        bot_profile_object = BotProfile.objects.create(
            user=user,
            title=title,
            first_name=first_name,
            last_name=last_name,
            address_1=address_1,
            address_2=address_2,
            phone_number=phone_number,
            country=country,
            state=state,
            city=city,
            zip=zip
        )
        bot_profile_object.save()
        return Response(status=HTTP_201_CREATED)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_bot_profile(request, bot_profile_id):
    try:
        bot_profile_object = BotProfile.objects.get(id=bot_profile_id)
        if(bot_profile_id):
            user = request.user
            if(bot_profile_object.user==user):
                serializer = BotProfileSerializer(instance=bot_profile_object, data=request.data, partial=True)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(status=HTTP_200_OK)
                return Response(status=HTTP_206_PARTIAL_CONTENT)
            return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(status=HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({"error": f"{error}"},status=HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_bot_profile(request, bot_profile_id):
    try:
        bot_profile_object = BotProfile.objects.get(id=bot_profile_id)
        if(bot_profile_id):
            user = request.user
            if(bot_profile_object.user==user):
                bot_profile_object.delete()
                return Response(status=HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)