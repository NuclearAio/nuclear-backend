import datetime
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


from .models import (
    Proxy, ProxyType, ProxyVendor,
    ProxiesExpense, UserProxyExpenseByVendor,
    UserProxiesPerformance
)
from .serializers import (
    ProxySerializer,
    ProxyVendorSerializer,
    ProxyTypeSerializer,
    ProxiesExpenseSerializer,
    UserProxyExpenseByVendorSerializer,
    UserProxiesPerformanceSerializer
)

@api_view(['GET'])
def get_proxy_vendors(request):
    try:
        proxy_vendor_objects = ProxyVendor.objects.all()
        serializer = ProxyVendorSerializer(proxy_vendor_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_proxy_types(request):
    try:
        proxy_type_object = ProxyType.objects.all()
        serializer = ProxyTypeSerializer(proxy_type_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_proxies(request):
    try:
        user = request.user
        paginator = PageNumberPagination()
        paginator.page_size = 1
        proxy_objects  = Proxy.objects.filter(user=user)
        paginated_objects = paginator.paginate_queryset(proxy_objects, request)
        serializer = ProxySerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)


# Add the test for this 
@api_view(['GET'])
def get_proxies_by_current_month(request):
    try:
        current_time = datetime.datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        proxy_objects = Proxy.objects.filter(user=request.user, created_at__gte=datetime.date(current_year, current_month, 1))
        if(not proxy_objects):
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = ProxySerializer(proxy_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_proxies_by_current_week(request):
    try:
        current_week = datetime.date.today().isocalendar()[1] 
        proxy_objects = Proxy.objects.filter(user=request.user, created_at__week=current_week)
        if(not proxy_objects):
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = ProxySerializer(proxy_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

"""Add filter by year as weel"""
""" REFACTOR """
@api_view(['POST'])
def create_proxy(request):
    try:
        user = request.user
        data = request.data
        proxy_vendor_id = data.get('proxy_vendor_id')
        proxy_type_id = data.get('proxy_type_id')
        title = data.get('title')
        ip_address = data.get('ip_address')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        cost = data.get('cost')

        proxy_vendor_object = ProxyVendor.objects.get(id=proxy_vendor_id)
        proxy_type_object = ProxyType.objects.get(id=proxy_type_id)
        if(proxy_vendor_object):
            proxy_object = Proxy.objects.create(
                user=user,
                title=title,
                ip_address=ip_address,
                port=port,
                username=username,
                password=password,
                cost=cost
            )
            proxy_object.proxy_vendor = proxy_vendor_object
            proxy_object.proxy_type = proxy_type_object
            proxy_object.save()
            
            try:
                obj = UserProxyExpenseByVendor.objects.get(user=user, proxy_vendor=proxy_vendor_object)
                obj.spent= F('spent') + cost
                obj.save()
                    
            except ObjectDoesNotExist:
                obj = UserProxyExpenseByVendor(
                    user=user,
                    proxy_vendor=proxy_vendor_object,
                    spent=cost
                )
                obj.save()

            try:
                proxy_expense_object = ProxiesExpense.objects.get(user=request.user)
                proxy_expense_object.expense = F('expense') + cost
                proxy_expense_object.save()
            except ObjectDoesNotExist:
                proxy_expense_object = ProxiesExpense(
                    user=user,
                    expense=cost
                )
                proxy_expense_object.save()

            """ Updating Global Vendor decline/success/number_of_time_proxy_get_used is done inside create_report view"""

            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_206_PARTIAL_CONTENT)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

"""
{
    "proxy_vendor_id": "f8c4c4a9-adad-4eae-b9c3-49bd0c6c616c,
    "proxy_type_id": "71b0cbfa-a7cf-4ad8-9761-0ac80de21984",
    "title": "Hello Proxy",
    "ip_address": "123.456.23.45",
    "cost": 23
}
"""   


@api_view(['GET'])
def get_user_proxies_expense_by_vendors(request):
    try:
        expense_by_vendors_object = UserProxyExpenseByVendor.objects.filter(user=request.user)
        serializer = UserProxyExpenseByVendorSerializer(expense_by_vendors_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response(status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
def spent_on_proxies(request):
    # proxy price should be read only not edditable 
    try:
        proxy_expense_object = ProxiesExpense.objects.get(user=request.user)
        if(proxy_expense_object.user!=request.user):
            return Response(status=HTTP_401_UNAUTHORIZED)
        serializer  = ProxiesExpenseSerializer(proxy_expense_object)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_204_NO_CONTENT)



@api_view(['GET'])
def get_user_proxies_performance(request):
    try:
        user_proxy_performace = UserProxiesPerformance.objects.filter(user=request.user)
        serializer = UserProxiesPerformanceSerializer(user_proxy_performace, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=HTTP_204_NO_CONTENT)