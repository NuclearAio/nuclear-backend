from django.urls import path

from .views import (
    get_sites,
    create_report,
    get_reports,
    get_amount_spent_by_bot_on_shoes
)
urlpatterns = [
    path('supported_sites/', get_sites, name="get_sites_for_report_building"),
    path('create/', create_report, name="create_report"),
    path('reports/', get_reports, name="get_reports"),
    path('amount_spent_by_bot/', get_amount_spent_by_bot_on_shoes, name="amount_spent_by_bot_on_shoes")
]