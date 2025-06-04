from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, UserList

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserView.as_view()),
    path('user-list/', UserList.as_view()),
    path('logout/', LogoutView.as_view()),
]