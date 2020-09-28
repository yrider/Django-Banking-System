from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm
from django.contrib import messages


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = 'transactions'

    def get_context_data(self, **kwargs):
        data = super(LoginView, self).get_context_data(**kwargs)
        data['title'] = 'Login'
        return data

    def form_valid(self, form):
        request = self.request

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            messages.success(request, 'You are now logged in.')
            login(request, user)
            if is_safe_url(self.success_url, request.get_host()):
                return redirect(self.success_url)
            else:
                return redirect('/')
        else:
            return super(LoginView, self).form_invalid(form)

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = 'login'

    def get_context_data(self, **kwargs):
        data = super(RegisterView, self).get_context_data(**kwargs)
        data['title'] = 'Register'
        return data

    def form_valid(self, form):
        request = self.request
        registration_form = RegisterForm(request.POST)
        user = registration_form.save()
        messages.success(
            request,
            'Thank you for creating a bank account. '
            f'Your account number is {user.account.account_no}. '
            'You can now login.'
        )
        return redirect(self.success_url)
