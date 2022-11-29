from django.db import models
from users.generator import hash_password
from activities.models import ClassType, Subject, Department
from django.utils import timezone
from django.db import models, IntegrityError, transaction

# Create your models here.

class Parent(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=13, unique=True, blank=False)
    address = models.CharField(max_length=200, blank=True)
    status = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name}'
    

class Student(models.Model):
    GENDER_CHOICE = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE")
    )
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
    gender = models.CharField(max_length=50, choices=GENDER_CHOICE, null=False, blank=False)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student_class = models.ForeignKey(ClassType, on_delete=models.SET_NULL, null=True)
    dob = models.DateField()
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.first_name}{self.last_name} {self.student_class.name}'
    


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

                student = cls.objects.create(**kwargs)
                student_profile = StudentProfile.create_student_profile(
                    user_id = user_id,
                    first_name = kwargs["first_name"],
                    last_name = kwargs["last_name"],
                    middle_name = kwargs["middle_name"],
                    email = kwargs["email"], 
                    parent=kwargs["parent"],
                    phone_number=phone_number,
                    student = student,
                    pin=pin,
                    # account_type=account_type,
                )
                print(f"student profile {student_profile}")

                if student_profile:
                    return student
                
                else:
                    transaction.set_rollback(True)
                    return None
            
            except IntegrityError as e:
                return {"student": None, "message": e.args[0]}

class StudentProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    user_id = models.CharField(unique=True, max_length=50)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    # account_type=models.CharField(max_length=50, default="teacher", editable=False)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


    @classmethod
    def create_student_profile(cls, **kwargs):
        # print('preofile', kwargs)
        with transaction.atomic():
            try:
                student_profile = cls(
                    user_id=kwargs["user_id"],
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    middle_name=kwargs["middle_name"],
                    parent=kwargs["parent"],
                    student=kwargs["student"],
                    email = kwargs["email"], 
                    phone_number=kwargs["phone_number"],
                )

                student_profile.save()


                StudentProfileLogin.create_login(
                    user_id=kwargs["user_id"],
                    pin=kwargs["pin"],
                    student_profile=student_profile,
                    first_name=kwargs["first_name"],
                    last_name=kwargs["last_name"],
                    # middle_name=kwargs["middle_name"],
                )


                return student_profile

            except IntegrityError as e:
                return {"student profile" : None, "message": e.args[0]}




class StudentProfileLogin(models.Model):
    user_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    pin = models.CharField(max_length=255, null=True, blank=True)
    student_profile = models.OneToOneField("StudentProfile", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    session_id = models.CharField(null=True, blank=True, max_length=250)


    @classmethod
    def create_login(cls, user_id, pin, first_name, last_name,  teacher_profile):
        hashed_password = hash_password(pin)
        cls(user_id=user_id, teacher_profile=teacher_profile, first_name=first_name, last_name=last_name, pin=hashed_password).save()


class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    attendance_time  = models.DateTimeField(auto_now=True, auto_now_add=False)



class AttendanceReport(models.Model):
    ATTENDANCE_CHOICES = (
        ("present", "present"),
        ("absent", "absent")
    )
    student  = models.ForeignKey("Student", on_delete=models.CASCADE)
    attendance = models.ForeignKey("Attendance", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, null=False)
    