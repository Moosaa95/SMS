from django.urls import path 
from .Endpoints import RegisterTeacherAPIView


urlpatterns = [
    path('add-teacher', RegisterTeacherAPIView.as_view(), name='add-teacher')
]
