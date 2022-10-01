from django.contrib import admin
from .models import (
    ProxyType,
    ProxyVendor,
    ProxiesExpense,
    UserProxyExpenseByVendor,
    UserProxiesPerformance,
    Proxy,
)

admin.site.register(ProxyType)
admin.site.register(ProxyVendor)
admin.site.register(ProxiesExpense)
admin.site.register(UserProxyExpenseByVendor)
admin.site.register(UserProxiesPerformance)
admin.site.register(Proxy)
