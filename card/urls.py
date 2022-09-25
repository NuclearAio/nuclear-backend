from django.urls import path

from .views import (
    get_cards,
    create_card,
    update_card,
    delete_card
)

urlpatterns = [
    path('cards/', get_cards, name="cards"),
    path('create/', create_card, name="create_card"),
    path('update/<str:card_id>/', update_card, name="update_card"),
    path('delete/<str:card_id>/', delete_card, name="delete_card"),
]