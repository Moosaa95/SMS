from django.db import models

# Create your models here.
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
# from student.models import Student
from teacher.models import Teacher

from users.models import Account, ModelMixin


class ClassType(models.Model):
    name = models.CharField(max_length=10, unique=True, db_index=True)
    department = models.CharField(max_length=50)
    form_master = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'
    
    @classmethod
    def get_teacher_account(cls, teacher_id):

        try:
            if teacher_id:
                teacher = Teacher.objects.filter(user_id=teacher_id).values(
                    "account_type"
                    )
            else:
                teacher = None 
        except Teacher.DoesNotExist as e:
            return {"message":f"does not exist see {e.args[0]}"}
        return teacher

    
    @classmethod
    def create_class(cls, **kwargs):
        print("=======================KWARGS========")
        print(kwargs)
        with transaction.atomic():
            try:
                # name = kwargs.get("name", None)
                # department = kwargs.get("department", None)
                # account_type = kwargs.get("account_type", None)
                user_id = kwargs.pop("form_master")
                teacher = None
                # account_type = cls.get_teacher_account(teacher_id=user_id)
                # # print('==========account type ====')
                # # print(account_type["account_type"])
                # account_type = account_type[0]["account_type"] if account_type else ""
                

                if user_id:
                    teacher = cls.get_teacher(user_id=user_id, obj=True)
                if teacher:
                    kwargs.update(
                        form_master=teacher
                    )
                
                    class_type = cls.objects.create(**kwargs)
                else:
                    raise Exception("not created")
                # print("---------class type")
                # print(class_type)

                if class_type:
                    return class_type
                else:
                    return transaction.rollback(True)
            except IntegrityError as e:
                return {'class':None, 'message':e.args[0]}
    
    @classmethod
    def get_teacher(cls, **kwargs):
        obj = kwargs.pop("obj", None)
        try:
            if obj:
                teacher = Teacher.objects.get(**kwargs)
            else:
                teacher = Teacher.objects.get(**kwargs)
        except Teacher.DoesNotExist:
            teacher = None 
        
        return teacher


class Department(models.Model):
    dept_code = models.CharField(max_length=10, unique=True)
    dept_name = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.dept_code} -- {self.dept_name}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    teacher = models.ManyToManyField(Teacher, related_name="teacher_subject")
    

    def __str__(self):
        return f'{self.subject_name}'
    

