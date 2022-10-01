from django.urls import path

from .views import (
    get_selling_mediums,
    create_inventory_item,
    update_inventory_item,
    get_inventory, 
    get_shoes_sold_this_week_month
)

urlpatterns = [
    path('selling_mediums/', get_selling_mediums, name="selling_mediums"),
    path('create/', create_inventory_item, name="create_inventory"),
    path('update/<str:inventory_item_id>/', update_inventory_item, name="update_inventory_item"),
    path('inventories/', get_inventory, name="get_inventory_of_user"),
    path('sold/', get_shoes_sold_this_week_month, name="shoes_sold_this_week_month"),
]
