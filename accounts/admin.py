from django.contrib.auth.models import Group
from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserBankAccount

admin.site.register(User)
admin.site.register(UserBankAccount)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
