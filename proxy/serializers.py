from rest_framework.serializers import ModelSerializer

from .models import (
    Proxy, ProxyType,
    ProxyVendor, ProxiesExpense,
    UserProxyExpenseByVendor,
    UserProxiesPerformance

)
# Make Field read ONLY IF NESSESARY 
class UserProxyExpenseByVendorSerializer(ModelSerializer):

    class Meta:
        model = UserProxyExpenseByVendor
        fields = '__all__'


class ProxyVendorSerializer(ModelSerializer):

    class Meta:
        model = ProxyVendor
        fields = '__all__'


class ProxyTypeSerializer(ModelSerializer):

    class Meta:
        model = ProxyType
        fields = '__all__'


class ProxiesExpenseSerializer(ModelSerializer):

    class Meta:
        model = ProxiesExpense
        fields = '__all__'


class UserProxiesPerformanceSerializer(ModelSerializer):
    proxy_vendor = ProxyVendorSerializer(read_only=True)

    class Meta:
        model = UserProxiesPerformance
        fields = ['id', 'proxy_vendor', 'number_of_time_vendor_get_used', 'total_success', 'number_of_decline']

class ProxySerializer(ModelSerializer):
    proxy_vendor = ProxyVendorSerializer(read_only=True)
    proxy_type = ProxyTypeSerializer(read_only=True)

    class Meta:
        model = Proxy
        fields = ['id', 'proxy_vendor', 'proxy_type', 'title', 'ip_address', 'port', 'username', 'password', 'cost', 'created_at']
