from django.urls import path
from .views import register_view, login_view, get_profile

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('profile/', get_profile),
]
