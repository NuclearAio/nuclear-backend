from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', include('bot_profile.urls')),
    path('card/', include('card.urls')),
    path('proxy/', include('proxy.urls')),
    path('bot/', include('bot.urls')),
    path('report/', include('report.urls')),
    path('inventory/', include('inventory.urls')),
    path('account/', include('account.urls')),
]
