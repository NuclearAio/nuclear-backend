from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND,
    HTTP_206_PARTIAL_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_226_IM_USED
)

from .models import (
    BotVendor,
    BotSubscription,
    
)
from .serializers import (
    BotSubscriptionSerializer,
    BotVendorSerializer,
    BotSubscription
)

# All bots Vendor
@api_view(['GET'])
def get_bot_vendors(request):
    try:
        bot_vendor_object = BotVendor.objects.all()
        serializer = BotVendorSerializer(bot_vendor_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

# All bot vendor with pagination
@api_view(['GET'])
def get_bots_success_rate(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 6
        bot_vendor_objects = BotVendor.objects.all()
        paginated_objects =  paginator.paginate_queryset(bot_vendor_objects, request)
        serializer = BotVendorSerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response(status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_bot_subscription(request):
    try:
        user=request.user
        data=request.data
        bot_vendor_id = data.get('bot_vendor_id')
        one_time_cost = data.get('one_time_cost')
        cost = data.get('cost')

        bot_vendor_object = BotVendor.objects.get(id=bot_vendor_id)
        try:
            bot_subscription_object = BotSubscription.objects.get(user=user, bot_vendor=bot_vendor_object)
            if(bot_subscription_object):
                return Response({"error": "This bot subscription is already exist!"}, status=HTTP_226_IM_USED)
        except ObjectDoesNotExist:
            bot_subscription_object = BotSubscription.objects.create(
                    user=user,
                    one_time_cost=one_time_cost,
                    cost=cost
                )
            bot_subscription_object.bot_vendor=bot_vendor_object
            bot_subscription_object.save()
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_200_OK)

    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_bot_subscriptions(request):
    try:
        bot_subscription_object = BotSubscription.objects.filter(user=request.user, still_subscribed=True)
        serializer = BotSubscriptionSerializer(bot_subscription_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_bot_subscription(request, bot_subscription_id):
    try:
        bot_subscription_object = BotSubscription.objects.get(id=bot_subscription_id)
        if(bot_subscription_object):
            if(bot_subscription_object.user!=request.user):
                return Response(status=HTTP_401_UNAUTHORIZED)
            bot_subscription_object.delete()
        return Response(status=HTTP_204_NO_CONTENT)    
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_bot_performance(reequest):
    pass