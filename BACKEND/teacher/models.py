from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Address(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    housenumber = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.state} {self.city}'

    class Meta:
        verbose_name_plural = 'Addresses'
    


class Teacher(models.Model):
    email = models.EmailField()
    phone_number = PhoneNumberField(max_length=15)
    name = models.CharField(max_length=75)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    post = models.CharField(max_length=100, null=True)
    dob = models.DateField()

    def __str__(self):
        return f'{self.name}'


class Class(models.Model):
    name = models.CharField(max_length=10, unique=True, db_index=True)
    department = models.CharField(max_length=50)
    form_master = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'
    

class Subject(models.Model):
    subject = models.CharField(max_length=50)
    teacher = models.ManyToManyField(Teacher)
    class_taken = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.subject}'
    
