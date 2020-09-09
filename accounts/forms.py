from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, UserBankAccount
from django.db import transaction

class RegisterForm(UserCreationForm):
    GENDER_CHOICE = ('M', 'Male'), ('F', 'Female')

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    contact_no = forms.CharField(widget=forms.NumberInput, label="Mobile Number")
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField()
    annual_income = forms.CharField(widget=forms.NumberInput)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    balance = forms.IntegerField(label="Starting Account Balance")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            contact_no = self.cleaned_data.get('contact_no')
            gender = self.cleaned_data.get('gender')
            annual_income = self.cleaned_data.get('annual_income')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            balance = self.cleaned_data.get('balance')
            birth_date = self.cleaned_data.get('birth_date')

            UserBankAccount.objects.create(
                user = user,
                contact_no = contact_no,
                gender = gender,
                annual_income = annual_income,
                birth_date = birth_date,
                street_address = street_address,
                city = city,
                postal_code = postal_code,
                country = country,
                balance = balance,
                account_no = settings.ACCOUNT_NUMBER_START_FROM + user.id
            )
        return user

class LoginForm(forms.Form):

    email = forms.EmailField(label="email")
    password = forms.CharField(
        widget=forms.PasswordInput
    )