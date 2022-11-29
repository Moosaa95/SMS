from django.shortcuts import render
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings 
import requests
from .models import *
from django.utils import timezone
import json
from rest_framework.parsers import FileUploadParser, FormParser
from .serializers import AccountSerializer
from .generator import generate_user_id
from django.core.mail import send_mail

# Create your views here.


# {"first_name": "moosa", "last_name": "yayx", "middle_name": "omeiza", "email": "moosaabdullahi@gmail.com", "address": "omille", "state": "abuja", "country": "Nigeria", "account_type": "teacher", "phone_number":"90676454545"}


class RegisterUserAPIView(APIView):

    # parser_classes = [FileUploadParser, FormParser]
    
    def post(self, request, format=None):
        print('outside')
        # if request.method == 'POST':
        print('inside')
        pin = get_random_string(length=6, allowed_chars="1234567890")
        # user_id = request.data.get("user_id", None)
        # user_id = generate_user_id()

        account_type=request.data.get("account_type"),
        print(account_type)
        user_id=generate_user_id(length=4, account_type=account_type[0]),
        message = (
            f"You have been added to the {account_type} dashboad, check for otp",
            f"login with your user_id and password"
            f"user_id: {user_id} \n Pin:{pin}"
        )
        # data = (request.data)
        # new_data = json.loads(data)
        # serialize = AccountSerializer(data=data)
        # print("******************")
        # # print(serialize.is_valid)
        # # print(request.data, dir(request))
        # print("==========")
        
        new_user = Account.create_account_user(
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            middle_name=request.data.get("middle_name"),
            email=request.data.get("email"),
            address=request.data.get("address"),
            state=request.data.get("state"),
            country=request.data.get("country"),
            account_type=account_type,
            user_id=user_id[0],
            phone_number=request.data.get("phone_number"),
            pin=pin
        )
        print(new_user)

        if new_user and type(new_user) is not dict:
            mail_data = dict(
                name = request.data.get("first_name", None),
                recipient_form = request.data.get("email", None),
                subject="YourOTP",
                message=message, 

            )
            togun = send_mail(**mail_data)
            print('topgun', togun)

            # create_user2(
            #     user_id=new_agent.id,
            #     email=request.data.get("email"),
            #     user_type="agent",
            #     permissions=["agent"],
            #     status=True,
            # )
            return JsonResponse(data={"status": True})
        else:
            return JsonResponse(data={"status": False})#, "message": new_agent["message"]})
