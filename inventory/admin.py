from django.contrib import admin

from .models import (
    SellingMedium,
    Sold, UnSold,
    Inventory
)

admin.site.register(SellingMedium)
admin.site.register(Sold)
admin.site.register(UnSold)
admin.site.register(Inventory)