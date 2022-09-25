from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT,
    HTTP_206_PARTIAL_CONTENT,
)

from .models import Card
from .serializers import CardSerializer


@api_view(['GET'])
def get_cards(request):
    try: 
        user = request.user
        paginator = PageNumberPagination()
        paginator.page_size = 1
        card_objects  = Card.objects.filter(user=user)
        paginated_objects = paginator.paginate_queryset(card_objects, request)
        serializer = CardSerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_card(request):
    try:
        user = request.user
        data = request.data
        title = data.get('title')
        card_number = data.get('card_number')
        last_four_digit = data.get('last_four_digit')
        note = data.get('note')

        card_object = Card.objects.create(
            user=user,
            title=title,
            card_number=card_number,
            last_four_digit=last_four_digit,
            note=note
        )
        card_object.save()
        return Response(status=HTTP_201_CREATED)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_card(request, card_id):
    try:
        card_object = Card.objects.get(id=card_id)
        if(card_object):
            user = request.user
            if(card_object.user==user):
                serializer = CardSerializer(instance=card_object, data=request.data, partial=True)
                if(serializer.is_valid()):
                    serializer.save()
                    return Response(status=HTTP_200_OK)
                return Response(status=HTTP_206_PARTIAL_CONTENT)
            return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(status=HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({"error": f"{error}"},status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_card(request, card_id):
    try:
        card_object = Card.objects.get(id=card_id)
        if(card_object):
            user = request.user
            if(card_object.user==user):
                card_object.delete()
                return Response(status=HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)