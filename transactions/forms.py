from django import forms
from django.forms import ModelForm
from .models import Transaction

class TransactionForm(ModelForm):
    
    class Meta:
        model = Transaction
        fields = ('amount', 'transaction_type')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount < 0:
            raise forms.ValidationError("You cannot insert a negative monetary value.")
        elif amount > 5000:
            raise forms.ValidationError(f"Sorry, £{amount} exceeds our unauthorised transaction " 
                                        "limit. Please contact your local branch directly if you "
                                        "would like to continue with this transaction.")
        return amount

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.account = self.request
        self.instance.new_balance = self.request.balance
        return super().save()