from django.shortcuts import render
from django.views.generic import CreateView, FormView, DetailView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class DepositView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'transactions/deposits.html', {'title': 'Deposits'})

class LoanView(View):
    def get(self, request):
        return render(request, 'transactions/loans.html', {'title': 'Loans'})

class TransactionView(View):
    def get(self, request):
        return render(request, 'transactions/transDetails.html', {'title': 'Transactions'})

class WithdrawalView(FormView):
    def get(self, request):
        return render(request, 'transactions/withdrawals.html', {'title': 'Withdrawals'})

class TransferView(FormView):
    def get(self, request):
        return render(request, 'transactions/transfers.html', {'title': 'Transfers'})
