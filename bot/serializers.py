from pkgutil import read_code
from rest_framework.serializers import ModelSerializer

from .models import (
    BotVendor,
    BotSubscription,
)

class BotVendorSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = BotVendor

class BotSubscriptionSerializer(ModelSerializer):
    bot_vendor = BotVendorSerializer(read_only=True)

    class Meta:
        fields = ['id', 'bot_vendor', 'one_time_cost', 'cost', 'still_subscribed']
        model = BotSubscription