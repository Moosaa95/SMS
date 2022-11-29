from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
import hashlib
import binascii
import smtplib
import random
import string
import json
from django.db import models, IntegrityError, transaction
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail

from users.models import Account, ModelMixin, ProfileLogin
from users.generator import generate_user_id, hash_password


# Create your models here.



class Teacher(models.Model):
    # user_id = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    can_login_web = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    today_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # account_type = models.CharField(max_length=20, default="teacher", editable=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    @classmethod
    def create_teacher_account(cls, **kwargs):
        with transaction.atomic():
            try:
                pin = kwargs.pop("pin")
                user_id = kwargs.pop("user_id")
                # print(f'inside model fo4r user {user_id}')
                phone_number = kwargs.get("phone_number", None)
                account_type = kwargs.get("account_type", None)
                # parent=None 
                # student = None 
                # teacher = None 

                teacher = cls.objects.create(**kwargs)
                teacher_profile = TeacherProfile.create_teacher_profile(
                    user_id = user_id,
                    first_name = kwargs["first_name"],
                    last_name = kwargs["last_name"],
                    middle_name = kwargs["middle_name"],
                    email = kwargs["email"], 
                    phone_number=phone_number,
                    teacher = teacher,
                    pin=pin,
                    # account_type=account_type,
                )
                print(f"teacher profile {teacher_profile}")

                if teacher_profile:
                    return teacher
                
                else:
                    transaction.set_rollback(True)
                    return None
            
            except IntegrityError as e:
                return {"teacher": None, "message": e.args[0]}

class TeacherProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    user_id = models.CharField(unique=True, max_length=50)
    # account_type=models.CharField(max_length=50, default="teacher", editable=False)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


    @classmethod
    def create_teacher_profile(cls, **kwargs):
        # print('preofile', kwargs)
        with transaction.atomic():
            try:
                teacher_profile = cls(
                    user_id=kwargs["user_id"],
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    middle_name=kwargs["middle_name"],
                    # account_type=kwargs["account_type"],
                    teacher=kwargs["teacher"],
                    email = kwargs["email"], 
                    phone_number=kwargs["phone_number"],
                )

                teacher_profile.save()


                TeacherProfileLogin.create_login(
                    user_id=kwargs["user_id"],
                    pin=kwargs["pin"],
                    teacher_profile=teacher_profile,
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    # middle_name=kwargs["middle_name"],
                )


                return teacher_profile

            except IntegrityError as e:
                return {"teacher profile" : None, "message": e.args[0]}




class TeacherProfileLogin(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    # middle_name = models.CharField(max_length=50)
    pin = models.CharField(max_length=255, null=True, blank=True)
    teacher_profile = models.OneToOneField("TeacherProfile", on_delete=models.CASCADE)
    # profile = models.OneToOneField(teacher.Teacher, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    session_id = models.CharField(null=True, blank=True, max_length=250)


    @classmethod
    def create_login(cls, user_id, pin, first_name, last_name,  teacher_profile):
        hashed_password = hash_password(pin)
        cls(user_id=user_id, teacher_profile=teacher_profile, first_name=first_name, last_name=last_name, pin=hashed_password).save()




                


# # class Subject(models.Model):
# #     subject = models.CharField(max_length=50)
# #     teacher = models.ManyToManyField(Teacher)
# #     class_taken = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

# #     def __str__(self):
# #         return f'{self.subject}'
    
