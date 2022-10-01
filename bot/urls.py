from django.urls import path
from .views import (
    get_bot_vendors,
    create_bot_subscription,
    get_bot_subscriptions, 
    delete_bot_subscription
)

urlpatterns = [
    path('vendors/', get_bot_vendors, name="get_all_bot_vendors"),
    path('subscriptions/', get_bot_subscriptions, name="get_bot_subscription"),
    path('create_subscription/', create_bot_subscription, name="create_bot_subscription"),
    path('delete_subscription/<str:bot_subscription_id>/', delete_bot_subscription, name="create_bot_subscription"),
]