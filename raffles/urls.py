from django.urls import path
from .views import RaffleCreateView

urlpatterns = [
    path('create-raffle/', RaffleCreateView.as_view()),
]