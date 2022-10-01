import datetime
from email.policy import HTTP
from socket import AI_PASSIVE
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND,
    HTTP_206_PARTIAL_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR,
)

from .models import SellingMedium, Sold, UnSold, Inventory
from .serializers import InventorySerializer, SellingMediumSerializer

@api_view(['GET'])
def get_selling_mediums(request):
    try:
        selling_medium_object = SellingMedium.objects.all()
        serializer = SellingMediumSerializer(selling_medium_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_inventory_item(request):
    try:
        user=request.user
        data=request.data
        product_name=data.get('product_name')
        product_size=data.get('product_size')
        buying_price=data.get('buying_price')
        selling_price=data.get('selling_price')
        delivery_rate=data.get('delivery_rate')
        selling_medium_id=data.get('selling_medium_id')
        is_sold=data.get('is_sold')

        if(is_sold):
            selling_medium_object = SellingMedium.objects.get(id=selling_medium_id)
            inventory_object = Inventory(
                user=user,
                product_name=product_name,
                product_size=product_size,
                buying_price=buying_price,
                selling_price=selling_price,
                delivery_rate=delivery_rate,
                is_sold=True
            )
            inventory_object.selling_medium = selling_medium_object
            inventory_object.save()

            try:
                total_revenue_from_shoes_sales = Sold.objects.get(user=user)
                total_revenue_from_shoes_sales.amount = F('amount') + selling_price
                total_revenue_from_shoes_sales.save()
            except ObjectDoesNotExist:
                total_revenue_from_shoes_sales = Sold(
                    user=user,
                    amount=selling_price
                )
                total_revenue_from_shoes_sales.save()

        if(not is_sold):
            inventory_object = Inventory(
                user=user,
                product_name=product_name,
                buying_price=buying_price,
                is_sold=False
            )
            inventory_object.save()

            try:
                total_spent_on_unsold_shoes_object = UnSold.objects.get(user=user)
                total_spent_on_unsold_shoes_object.amount = F('amount') + buying_price
                total_spent_on_unsold_shoes_object.save()
            except ObjectDoesNotExist:
                total_spent_on_unsold_shoes_object = UnSold(
                    user=user,
                    amount=buying_price
                )
                total_spent_on_unsold_shoes_object.save()

        return Response(status=HTTP_201_CREATED)

    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

# qs sghould be True or False
# http://127.0.0.1:8000/inventory/inventories/?is_sold=True/False
@api_view(['GET'])
def get_inventory(request):
    try:
        qs = request.query_params.get('is_sold')
        user = request.user
        paginator = PageNumberPagination()
        paginator.page_size = 2
        if(qs):
            inventory_objects = Inventory.objects.filter(user=user, is_sold=qs)
        else:
            inventory_objects = Inventory.objects.filter(user=user)

        paginated_objects = paginator.paginate_queryset(inventory_objects, request)
        serializer = InventorySerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

# ?filter=week/month
# Reveneu will be calculated in frontend 
@api_view(['GET'])
def get_shoes_sold_this_week_month(request):
    try:
        qs = request.query_params.get('filter')
        user=request.user
        current_time = datetime.datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        current_week = datetime.date.today().isocalendar()[1] 
        if(qs=="week"):
            inventory_objects = Inventory.objects.filter(user=user, is_sold=True, created_at__week=current_week)
        elif(qs=="month"):
            inventory_objects = Inventory.objects.filter(user=user, is_sold=True, created_at__gte=datetime.date(current_year, current_month, 1))
        else:
            return Response({"error": "Please include query_param /?= week or month"}, status=HTTP_204_NO_CONTENT)
        
        serializer = InventorySerializer(inventory_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_inventory_item(request, inventory_item_id):
    try:
        user=request.user
        data=request.data

        selling_price = data.get('selling_price')
        selling_medium_id = data.get('selling_medium_id')
        delivery_rate = data.get('delivery_rate')
        is_sold = data.get('is_sold')

        if(not is_sold):
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

        selling_medium_object = SellingMedium.objects.get(id=selling_medium_id)
        inventory_object = Inventory.objects.get(user=user, id=inventory_item_id)

        inventory_object.selling_price = selling_price
        inventory_object.selling_medium = selling_medium_object
        inventory_object.delivery_rate = delivery_rate
        inventory_object.is_sold = True
        inventory_object.save()

        """Removing buying ammount from the UnSold model because this shoes get sold ! and add to the sold model of user, if not present create model"""
        try:
            total_spent_on_unsold_shoes_object = UnSold.objects.get(user=user)
            total_spent_on_unsold_shoes_object.amount = F('amount') - inventory_object.buying_price
            total_spent_on_unsold_shoes_object.save()
        except Exception as error:
            return Response({"error": f"{error}"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            total_revenue_from_shoes_sales = Sold.objects.get(user=user)
            total_revenue_from_shoes_sales.amount = F('amount') + selling_price
            total_revenue_from_shoes_sales.save()
        except ObjectDoesNotExist:
            total_revenue_from_shoes_sales = Sold(
                user=user,
                amount=selling_price
            )
            total_revenue_from_shoes_sales.save()
        return Response(status=HTTP_200_OK)

    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)


# Create inventory item
"""
{
    "product_name" : "Nike Dunks",
    "product_size" : 12.5,
    "buying_price" : 156,
    "selling_price" : 299,
    "delivery_rate" : 15,
    "selling_medium_id" :"3c09f146-b5d8-4e9f-98d3-a7653b245d2c",
    "is_sold" : true
}
"""

# Inventory Item Update
"""
{
    "selling_price" : 299,
    "delivery_rate" : 15,
    "selling_medium_id" : "3c09f146-b5d8-4e9f-98d3-a7653b245d2c",
    "is_sold" : true
}
"""