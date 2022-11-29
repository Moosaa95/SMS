from django.contrib import admin
from .models import *
# # Register your models here.


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name')

@admin.register(TeacherProfile)
class TeacherProfile(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user_id')

@admin.register(TeacherProfileLogin)
class TeacherProfileLogin(admin.ModelAdmin):
    list_display = ("user_id", )

# # class SubjectAdmin(admin.ModelAdmin):
# #     list_display = ('class_taken', 'subject')
# admin.site.register(Class)
# # admin.site.register(Subject, SubjectAdmin)
# # admin.site.register(Address)
# # admin.site.register(Teacher, TeacherAdmin)


