import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT,
     HTTP_500_INTERNAL_SERVER_ERROR,
)
from bot_profile.models import BotProfile
from card.models import Card
from proxy.models import Proxy, UserProxiesPerformance, ProxyVendor
from bot.models import BotSubscription, UserBotPerformance, BotVendor 
from .models import Site, Report, SpentOnShoes
from .serializers import SiteSerializer, ReportSerializer, BotSpentOnShoesSerializer

@api_view(['GET'])
def get_sites(request):
    try:
        site_object = Site.objects.all()
        serializer = SiteSerializer(site_object, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_report(request):
    try:
        user=request.user
        data=request.data
        site_id = data.get('site')
        product_name=data.get('product_name')
        product_size=data.get('product_size')
        product_amount=data.get('product_amount')
        is_success=data.get('is_success')
        profile_id=data.get('profile_id')
        card_id=data.get('card_id')
        proxy_id=data.get('proxy_id')
        bot_id=data.get('bot_id')

        site_obj = Site.objects.get(id=site_id)
        bot_profile_object = BotProfile.objects.get(id=profile_id)
        card_object = Card.objects.get(id=card_id)
        proxy_object = Proxy.objects.get(id=proxy_id)
        bot_object  = BotSubscription.objects.get(id=bot_id)

        report_object = Report(
            user=user,
            product_name=product_name,
            product_size=product_size,
            is_success=is_success,
            product_amount = product_amount
        )
        report_object.site = site_obj
        report_object.profile = bot_profile_object
        report_object.card = card_object
        report_object.proxy = proxy_object
        report_object.bot = bot_object
        report_object.save()
        
        """User Proxy performace"""
        try:
            user_proxy_performace_object = UserProxiesPerformance.objects.get(user=user, proxy_vendor=proxy_object.proxy_vendor)
            if(user_proxy_performace_object):
                user_proxy_performace_object.number_of_time_vendor_get_used = F('number_of_time_vendor_get_used') + 1
                if(is_success):
                    user_proxy_performace_object.total_success = F('total_success') + 1
                else:
                    user_proxy_performace_object.number_of_decline = F('number_of_decline') + 1
                user_proxy_performace_object.save()

        except ObjectDoesNotExist:
            user_proxy_performace_object = UserProxiesPerformance(
                user=user,
                proxy_vendor=proxy_object.proxy_vendor,
                number_of_time_vendor_get_used=1
            )
            if(is_success):
                user_proxy_performace_object.total_success = 1
                user_proxy_performace_object.number_of_decline = 0
            else:
                user_proxy_performace_object.total_success = 0
                user_proxy_performace_object.number_of_decline = 1
            user_proxy_performace_object.save()

        """Global Proxy Performace"""
        try:
            proxy_vendor_object = ProxyVendor.objects.get(id=proxy_object.proxy_vendor.id)
            proxy_vendor_object.number_of_time_proxy_used = F('number_of_time_proxy_used') + 1
            if(is_success):
                proxy_vendor_object.total_success = F('total_success') + 1
            else:
                proxy_vendor_object.total_success = F('number_of_decline') + 1
            proxy_vendor_object.save()
        except Exception as error:
            return Response({"error": "error while updating global proxy performance "}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        """User bots performance"""
        try:
            user_bot_performance_object = UserBotPerformance.objects.get(user=user, bot_vendor=bot_object.bot_vendor)
            if(user_bot_performance_object):
                user_bot_performance_object.number_of_time_bot_ran = F('number_of_time_bot_ran') + 1
                if(is_success):
                    user_bot_performance_object.total_success = F('total_success') + 1
                else:
                    user_bot_performance_object.number_of_decline = F('number_of_decline') + 1
                user_bot_performance_object.save()
        except ObjectDoesNotExist:
            user_bot_performance_object = UserBotPerformance(
                user=user,
                bot_vendor=bot_object.bot_vendor,
                number_of_time_bot_ran = 1
            )
            if(is_success):
                user_bot_performance_object.total_success = 1
                user_bot_performance_object.number_of_decline = 0
            else:
                user_bot_performance_object.total_success = 0
                user_bot_performance_object.number_of_decline = 1
            user_bot_performance_object.save()
                
        """Global bot perofrmace"""
        try:
            bot_vendor_object = BotVendor.objects.get(id=bot_object.bot_vendor.id)
            bot_vendor_object.number_of_time_bot_ran = F('number_of_time_bot_ran') + 1
            if(is_success):
                bot_vendor_object.total_success = F('total_success') + 1
            else:
                bot_vendor_object.number_of_decline = F('number_of_decline') + 1
            bot_vendor_object.save()
        except Exception as error:
            return Response({"error": "error while updating global bot performance "}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        """Total money spent on Shoes"""
        if(is_success):
            try:
                spent_on_shoes_object = SpentOnShoes.objects.get(user=user)
                spent_on_shoes_object.amount = F('amount') + product_amount
                spent_on_shoes_object.save()
            except ObjectDoesNotExist:
                spent_on_shoes_object = SpentOnShoes(
                    user=user,
                    amount=product_amount
                )
                spent_on_shoes_object.save()
            
        return Response(status=HTTP_201_CREATED)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

"""
some changes: api should look like this -> total succes, weekly success, monthly success
                                            total decline, weekly decline, monthly decline,
                                            get success tasks, get decline tasks
"""
# add pagination
@api_view(['GET'])
def get_reports(request):
    try:
        current_time = datetime.datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        current_week = datetime.date.today().isocalendar()[1] 

        qs = request.query_params.get('filter')
        user=request.user
        paginator = PageNumberPagination()
        paginator.page_size = 2
        if(qs=="week"):
            report_objects = Report.objects.filter(user=user, created_at__week=current_week)
        elif(qs=="month"):
            report_objects = Report.objects.filter(user=user, created_at__gte=datetime.date(current_year, current_month, 1))
        elif(qs=="success"):
            report_objects = Report.objects.filter(user=user, is_success=True)
        elif(qs=="decline"):
            report_objects = Report.objects.filter(user=user, is_success=False)
        else:
            report_objects = Report.objects.filter(user=user)

        paginated_objects = paginator.paginate_queryset(report_objects, request)
        serializer = ReportSerializer(paginated_objects, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response({"error": f"{error}"}, status=HTTP_400_BAD_REQUEST)

# Total Decline and succes this week and this month
@api_view(['GET'])
def get_amount_spent_by_bot_on_shoes(request):
    try:
        bot_spent_on_shoes = SpentOnShoes.objects.get(user=request.user)
        serializer = BotSpentOnShoesSerializer(bot_spent_on_shoes)
        return Response(serializer.data, status=HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=HTTP_204_NO_CONTENT)
"""
{
    "site" : "c2dac605-93e7-4404-8e38-58323d9ba63b",
    "product_name" : "Nike modal 2",
    "product_size" : 3.5,
    "product_amount" : 234.54,
    "is_success" : true,
    "profile_id" : "243fd30a-87fc-4f00-aed0-28e6dd27c1f4",
    "card_id" :"c63110db-878f-468b-bb16-78c619dee064",
    "proxy_id" : "f8fd62eb-1cb6-4fc3-8d06-f78df0bd564d",
    "bot_id" : "7b9d3595-1c7b-4197-b271-1cc8e7b413c0"
}
"""