from django.urls import path 
from .endpoints import *


urlpatterns = [
    path("add-class", RegisterClassAPIView.as_view(), name="add-class"),
    
]
