from django.db import models
from accounts.models import UserBankAccount

class Transaction(models.Model):
    CHOICES = ('W', 'Withdrawal'), ('D', 'Deposit')

    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name="transactions")
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    new_balance = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.CharField(choices=CHOICES, max_length=1)

    def __str__(self):
        return str(self.account.account_no)