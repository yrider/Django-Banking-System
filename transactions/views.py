from django.views.generic import CreateView, ListView
from django.contrib import messages
from .models import Transaction
from .forms import TransactionForm

class TransferView(CreateView):
    template_name = 'transactions/transfers.html'
    form_class = TransactionForm
    success_url = '/transfers/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request.user.account
        })
        return kwargs

    def form_valid(self, form):
           
        request = self.request
        amount = form.cleaned_data.get("amount")
        trans_type = form.cleaned_data.get("transaction_type")
        account = self.request.user.account

        if trans_type == "D":
            long_trans_type = 'Deposit'
            account.balance += amount
        elif trans_type == "W":
            long_trans_type  = 'Withdrawal'
            account.balance -= amount

        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            request,
            f"Your {long_trans_type} has been completed successfully. "            
            f"Your new balance is £{account.balance}." 
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(TransferView, self).get_context_data(**kwargs)
        data['title'] = 'Transfers'
        return data


class TransactionView(ListView):
    template_name = 'transactions/transDetails.html'
    model = Transaction

    def get_queryset(self):
        queryset = super(TransactionView, self).get_queryset()
        # No idea how the below works
        queryset = queryset.filter(account=self.request.user.account)
        return queryset

    def get_context_data(self, **kwargs):
        data = super(TransactionView, self).get_context_data(**kwargs)
        data['title'] = 'Transactions'
        return data