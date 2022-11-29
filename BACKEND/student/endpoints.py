from users.generator import generate_user_id
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings 
from .models import *
from django.utils import timezone



class RegisterStudentAPIView(APIView):

    def post(self, request):
        pin = get_random_string(length=6, allowed_chars="1234567890")
        account_type= "student"
        user_id = generate_user_id(length=4, account_type="student")
        message = (
            f"You have been added to the {account_type} dashboad, check for otp",
            f"login with your user_id and password"
            f"user_id: {user_id} \n Pin:{pin}"
        )
        new_student = Student.create_teacher_account(
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            middle_name=request.data.get("middle_name"),
            email=request.data.get("email"),
            address=request.data.get("address"),
            state=request.data.get("state"),
            country=request.data.get("country"),
            # account_type=account_type,
            gender=request.data.get("gender"),
            parent=request.data.get("parent"),
            student_class=request.data.get("student_class"),
            department=request.data.get("department"),
            user_id=user_id,
            phone_number=request.data.get("phone_number"),
            pin=pin
        )

        if new_student:
            return JsonResponse(data={"status":True, "message":"user successfully registered"}, safe=False)
        return JsonResponse(data={"status":False, "message":"user not added"})