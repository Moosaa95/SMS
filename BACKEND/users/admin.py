from django.contrib import admin
from users.models import User, Profile, ProfileLogin, Account


# Register your models here.

admin.site.register(User)
admin.site.register(ProfileLogin)
admin.site.register(Profile)
# admin.site.register(Account)


# @admin.display(description='Name')
# def upper_case_name(obj):
#     return (f"{(obj.first_name).upper()}{(obj.last_name).upper()}")
@admin.register(Account)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'created_at' )