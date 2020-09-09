from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Full name"
            }
        ),
        label= 'Your Full Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control", 
                "placeholder": "Email"
            }
        ),
        label= 'Email Address'
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                "placeholder": "Message" 
            }
        ),
        label="Your Message"
    )
