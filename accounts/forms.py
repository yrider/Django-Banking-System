from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, UserBankAccount


class RegisterForm(UserCreationForm):
    GENDER_CHOICE = ('M', 'Male'), ('F', 'Female')

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    contact_no = forms.IntegerField(widget=forms.NumberInput, label="UK Mobile Number (Starting With 07)")
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField()
    annual_income = forms.IntegerField(widget=forms.NumberInput, label="Annual Income (GBP)")
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=100)
    balance = forms.IntegerField(label="Starting Account Balance")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_contact_no(self):
        number = self.cleaned_data.get("contact_no")
        if not(9 < len(str(number)) < 11):
            raise forms.ValidationError("Your UK telephone number must be 11 digits long.")
        return number

    def clean_annual_income(self):
        income = self.cleaned_data.get("annual_income")
        if income < 0:
            raise forms.ValidationError("You cannot have annual income less than or equal to 0.")
        return income

    def clean_balance(self):
        balance = self.cleaned_data.get("balance")
        if balance < 0:
            raise forms.ValidationError("You cannot open a new account with a negative balance.")
        return balance

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
                balance = balance,
                account_no = settings.ACCOUNT_NUMBER_START_FROM + user.id
            )
        return user

class LoginForm(forms.Form):

    email = forms.EmailField(label="email")
    password = forms.CharField(
        widget=forms.PasswordInput
    )
