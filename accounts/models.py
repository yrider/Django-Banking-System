import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractUser
)
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255, blank=False)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

class UserBankAccount(models.Model):
    GENDER_CHOICES = ('M', 'Male'), ('F','Female')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account'
    )
    contact_no = models.IntegerField(unique=True, null=True, blank=True)
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    birth_date = models.DateField(null=True, blank=True)
    annual_income = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(12)
        ]
    )
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100, null=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    REQUIRED_FIELDS = ['contact_no', 'account_no', 'gender', 'birth_date',
    'annual_income', 'street_address', 'city', 'postal_code']

    def __str__(self):
        return str(self.account_no)
