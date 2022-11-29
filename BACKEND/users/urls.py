from django.urls import path 
from .views import *



urlpatterns = [
    path("register", RegisterUserAPIView.as_view(), name="register-user")
]
