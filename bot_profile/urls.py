from django.urls import path

from .views import (
    delete_bot_profile,
    get_bot_profiles,
    create_bot_profile,
    update_bot_profile,
    delete_bot_profile
)

urlpatterns = [
    path('profiles/', get_bot_profiles, name="bot_profiles"),
    path('create/', create_bot_profile, name="create_bot_profile"),
    path('update/<str:bot_profile_id>/', update_bot_profile, name="update_bot_profile"),
    path('delete/<str:bot_profile_id>/', delete_bot_profile, name="delete_bot_profile"),
]