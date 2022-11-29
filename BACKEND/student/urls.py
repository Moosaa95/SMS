from django.urls import path 
from .endpoints import (
    RegisterStudentAPIView
    )


urlpatterns = [
    path('add-student', RegisterStudentAPIView.as_view(), name='add-student')
]
