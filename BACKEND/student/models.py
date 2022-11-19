from django.db import models
from teacher.models import Class, Address
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Parent(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField()
    phone_number = PhoneNumberField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f'{self.name}'
    

class Student(models.Model):
    name = models.CharField(max_length=75)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    dob = models.DateField()

    def __str__(self):
        return f'{self.name} {self.student_class.name}'
    

    