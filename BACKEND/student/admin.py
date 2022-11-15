from django.contrib import admin
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class')

    


admin.site.register(Student, StudentAdmin)
admin.site.register(Parent)

