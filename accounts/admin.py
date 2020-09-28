from django.contrib.auth.models import Group
from django.contrib import admin
from .models import User, UserBankAccount
from transactions.models import Transaction

admin.site.register(User)
admin.site.register(UserBankAccount)
admin.site.register(Transaction)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
