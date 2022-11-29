from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'student_class')

@admin.register(StudentProfile)
class StudentProfile(admin.ModelAdmin):
    list_display = ('user_id',)


@admin.register(StudentProfileLogin)
class StudentProfileLogin(admin.ModelAdmin):
    list_display = ('user_id',)


admin.site.register(Parent)