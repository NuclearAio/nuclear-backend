from django.contrib import admin
from .models import (
    BotVendor,
    UserBotPerformance,
    BotSubscription,
)

admin.site.register(BotVendor)
admin.site.register(UserBotPerformance)
admin.site.register(BotSubscription)
