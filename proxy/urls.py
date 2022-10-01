from django.urls import path

from .views import (
    create_proxy, get_proxies,
    get_proxy_vendors, get_proxy_types,
    spent_on_proxies,
    get_proxies_by_current_month, get_proxies_by_current_week,
    get_user_proxies_expense_by_vendors,
    get_user_proxies_performance
)

urlpatterns = [
    path('create/', create_proxy, name="create_proxy"),
    path('vendors/', get_proxy_vendors, name="proxy_vendor"),
    path('types/', get_proxy_types, name="proxy_types"),
    path('proxies/', get_proxies, name="get_proxies"),
    path('spent/', spent_on_proxies, name="total_amount_spent_on_proxies"),
    path('spent_on_vendors/', get_user_proxies_expense_by_vendors, name="total_amount_spent_with_vendors"),
    path('current_month/', get_proxies_by_current_month, name="current_month_proxies"),
    path('current_week/', get_proxies_by_current_week, name="current_week_proxies"),
    path('proxies_performace/', get_user_proxies_performance, name="user_proxies_performace"),
]