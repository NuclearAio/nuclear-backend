from rest_framework.serializers import ModelSerializer

from bot_profile.serializers import BotProfileSerializer
from card.serializers import CardSerializer
from proxy.serializers import ProxySerializer
from bot.serializers import BotSubscriptionSerializer

from .models import Site, Report, SpentOnShoes


class SiteSerializer(ModelSerializer):

    class Meta:
        model = Site
        fields = '__all__'


class BotSpentOnShoesSerializer(ModelSerializer):

    class Meta:
        model = SpentOnShoes
        fields ='__all__'


class ReportSerializer(ModelSerializer):
    site = SiteSerializer(read_only=True)
    profile = BotProfileSerializer(read_only=True)
    card = CardSerializer(read_only=True)
    proxy = ProxySerializer(read_only=True)
    bot = BotSubscriptionSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['site', 'product_name', 'product_size', 'is_success', 'profile', 'card', 'proxy', 'bot']