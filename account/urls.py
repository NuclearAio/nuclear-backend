from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import register, TokenObtainPairView
urlpatterns = [
    path('registration/', register, name="user_registration"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
