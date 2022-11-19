from django.contrib import admin
from .models import *
# Register your models here.


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name','post')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('class_taken', 'subject')


admin.site.register(Class)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Address)
admin.site.register(Teacher, TeacherAdmin)


