import hashlib
import binascii
import smtplib
import random
import string

from django.db import models, IntegrityError, transaction
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from .generator import generate_user_id
# from django.contrib.auth.models import (
#     PermissionsMixin, 
#     AbstractBaseUser, 
#     UserManager
# )
# from django.contrib.auth.hashers import make_password


# Create your models here.

def permission_default():
    return ["admin"]


def generate_random_code():
    return 'school_name'.join(random.choice(string.ascii_lowercase + string.digits, k=4))


# class MyUserManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not username:
#             raise ValueError("The given username must be set")

#         if not email:
#             raise ValueError("The given email must be set")
#         email = self.normalize_email(email)
#         # Lookup the real model class from the global app registry so this
#         # manager method can be used in migrations. This is fine because
#         # managers are by definition working on the real model.
#         # GlobalUserModel = apps.get_model(
#         #     self.model._meta.app_label, self.model._meta.object_name
#         # )
#         username = self.normalize_username(username)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(username, email, password, **extra_fields)

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(username, email, password, **extra_fields)




# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=20, unique=True)
#     # user_id = models.CharField(max_length=255, unique=True, null=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)

#     user_type = models.CharField(
#         max_length=255, choices=settings.USER_TYPES, default="teacher"
#     )
#     # date_joined = models.DateTimeField(default=)
#     email_verified = models.BooleanField(default=False)
    
#     objects = MyUserManager()

#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS= ['first_name', 'last_name']


#     @property
#     def token(self):
#         return ''
    

class ModelMixin(models.Model):
    profile = models.OneToOneField("Profile", on_delete=models.CASCADE)


    class Meta:
        abstract = True
class User(models.Model):
    
    user_id = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    status = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=255, choices=settings.USER_TYPES, default="teacher"
    )

    permissions = models.JSONField(default=permission_default, blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)

    objects = models.Manager()


    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    @classmethod
    def create_user(cls, **kwargs):
        new_user = cls(**kwargs)
        account_type = kwargs.pop("account_type")
        user_id = generate_user_id(length=4, account_type=account_type[0]),
        pin = get_random_string(length=6, allowed_chars="1234567890")
        message = settings.REG_MESSAGE % (kwargs["user_id"], pin)
        recipient = kwargs["email"]


        if not cls.email:
            raise ValueError('Users must have an email address')
        
        if not cls.password:
            raise ValueError('Users must have a password')

            

        try:
            response = send_mail(
                settings.SENDER_ID, message, settings.SENDER_EMAIL, [recipient]
            )
            if response == 1:
                new_user.user_id = user_id
                new_user.password = cls.hash_password(pin)
                try:
                    new_user.save()
                    message = f"User has been created successfully {pin}"
                    data = {"message"  :message, "status":True}
                except IntegrityError:
                    message = "Email already exist"
                    data = {"message" : message, "status":False}
            
            else:
                message = "User creation failed"
                data = {"message":message, "status":False}
        
        except smtplib.SMTPAuthenticationError:
            message = "user can not be added. Error! can't access mail server. check back or try again later"
            data = {"message":message, "status":False}
        
        return data 
    
    @classmethod
    def hash_password(cls, password):
        """
            Takes plain text password and return an encrypted hash password
        """
        encoded_password = password.encode()
        hasher = hashlib.pbkdf2_hmac("sha256", encoded_password, b"M0@s4", 1000)
        dechex = binascii.hexlify(hasher)
        hash_pass = dechex.decode()
        return hash_pass
    
    @classmethod
    def create_user2(cls, **kwargs):
        pin = kwargs.pop("pin", None) 
        if not pin:
            return None
        hashed_password = cls.hash_password(pin)
        kwargs.update(password=hashed_password)
        try:
            new_user = cls.objects.create(**kwargs)
            return new_user
        
        except IntegrityError as e:
            return None
    
    @property
    def token():
        return ''


class Account(models.Model):
    """
        model to store users bio data that use this platform
    """
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ("STUDENT", "STUDENT"),
        ("TEACHER","TEACHER"),
        ("PARENT","PARENT")
    )
    user_id = models.CharField(max_length=20,unique=True)
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
    account_type = models.CharField(default="", blank=False, null=False, max_length=50)
    # account_type = models.CharField(max_length=50, choices=REQUESTED_ACCOUNT_TYPE_CHOICES, blank=False, )
    teacher = models.ForeignKey(
        "Account", 
        related_name="account_teacher",
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        # to_field="teacher_id",
        # unique=True

    )
    student = models.ForeignKey(
        "Account", 
        related_name="account_student",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        
    )
    parent = models.ForeignKey(
        "Account", 
        related_name="account_parent",
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        
    )

    class Meta:
        ordering = ["pk"]
    
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    

   
    

    @classmethod
    def create_account_user(cls, **kwargs):
        print('create user', kwargs)
        with transaction.atomic():
            try:
                pin = kwargs.pop("pin")
                user_id = kwargs.get("user_id")
                phone_number = kwargs.get("phone_number", None)
                account_type = kwargs.get("account_type", None)
                # class_type = kwargs.pop("class_type", None)
                parent=None 
                student = None 
                teacher = None 
                account_type = account_type[0]
                if account_type == "student":
                    # print('student')
                    student = cls.get_account(
                        phone_number = phone_number, obj=True,
                        # account_type=account_type
                    )
                # # if student_id:
                # #     student = cls.get_account(
                # #         id=student_id, obj=True,
                # #         # account_type=account_type
                # #     )
                # gut = cls.objects.all()
                # # obj = cls.objects.get()
                # # print(obj.teacher_id, 'teacher')
                # print(gut, 'lp')
                if student:
                    kwargs.update(
                        student=student,
                        account_type="student"
                    )
                
                if account_type == "teacher":
                    teacher_id = cls.objects.values("teacher_id")
                    # print('before', teacher, teacher_id)
                    teacher = cls.get_account(
                        # teacher_id=56,
                        phone_number = phone_number, obj=True,
                        account_type="teacher"
                    )
                    print('after', teacher)
                
                # if teacher_id:
                #     teacher = cls.get_account(
                #         id=teacher_id, obj=True
                #     )
                if teacher:
                    print('inside teacher')
                    kwargs.update(
                        teacher=teacher, 
                        # account_type="teacher"
                    )
                
                if account_type == "parent":
                    parent = cls.get_account(
                        phone_number = phone_number, obj=True
                    )
                
                # if parent_id:
                #     parent = cls.get_account(
                #         id=parent_id, obj=True
                #     )
                if parent:
                    kwargs.update(
                        parent=parent, 
                        account_type="parent"
                    )
                print('saving kwargs', kwargs)
                account = cls.objects.create(**kwargs)
                # user_id = kwargs["user_id"]
                profile = Profile.create_profile(
                    user_id = user_id,
                    first_name = kwargs["first_name"],
                    last_name = kwargs["last_name"],
                    middle_name = kwargs["middle_name"],
                    email = kwargs["email"], 
                    phone_number=kwargs["phone_number"],
                    account = account,
                    pin=pin,
                    account_type=account_type,
                    # teacher=teacher,
                    # student=student,
                    # parent=parent

                )
                if profile:
                    return account 
                
                else:
                    transaction.set_rollback(True)
                    return None 
            except IntegrityError as e:
                return {"account" : None, "message" : e.args[0]}

                
    @classmethod
    def get_account(cls, **kwargs):
        print(kwargs)
        obj = kwargs.pop("obj", None)
        try:
            if obj:
                account = cls.objects.get(**kwargs)
            else:
                account = cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            account = None
        
        return account



class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    user_id = models.CharField(unique=True, max_length=50)
    account_type=models.CharField(max_length=50)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)


    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


    @classmethod
    def create_profile(cls, **kwargs):
        print('preofile', kwargs)
        with transaction.atomic():
            try:
                profile = cls(
                    user_id=kwargs["user_id"],
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    middle_name=kwargs["middle_name"],
                    account_type=kwargs["account_type"],
                    account=kwargs["account"],
                    email = kwargs["email"], 
                    phone_number=kwargs["phone_number"],
                )

                profile.save()


                ProfileLogin.create_login(
                    user_id=kwargs["user_id"],
                    pin=kwargs["pin"],
                    profile=profile,
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    middle_name=kwargs["middle_name"],
                )


                return profile

            except IntegrityError as e:
                return {"profile" : None, "message": e.args[0]}


class ProfileLogin(ModelMixin):
    user_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    pin = models.CharField(max_length=255, null=True, blank=True)
    # profile = models.OneToOneField(, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    session_id = models.CharField(null=True, blank=True, max_length=250)

   

    @classmethod
    def create_login(cls, user_id, pin, first_name, last_name, middle_name, profile):
        hashed_password = cls.hash_password(pin)
        cls(user_id=user_id, profile=profile, first_name=first_name, last_name=last_name, middle_name=middle_name, pin=hashed_password).save()


