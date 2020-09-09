from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import User


# WILL BE USED ONCE HOME PAGE IS CREATED
class ProfileView(View):
    def get(self, request):
        return render(request, 'accounts/profile.html', {'title': 'Profile'})

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = 'transactions'

    def form_valid(self, form):
        request = self.request

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            messages.success(request, f'You are now logged in.')
            login(request, user)
            if is_safe_url(self.success_url, request.get_host()):
                return redirect(self.success_url)
            else:
                return redirect('/')
        return super(LoginView, self).form_invalid(form)

class RegisterView(TemplateView):
    success_url = 'login'
    template_name = 'accounts/register.html'

    def get(self, request):
        form = RegisterForm
        context = {
            'form':form,
            'title':'Register'
        }
        return render(request, 'accounts/register.html', context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = RegisterForm(self.request.POST)

        if registration_form.is_valid():
            user = registration_form.save()
            #login(self.request, user)
            messages.success(
                self.request,
                (
                    'Thank you for creating a bank account. '
                    'Your account number is {}'.format(user.account.account_no)
                )
            )
            return redirect(self.success_url)
        return self.render_to_response(
            self.get_context_data(registration_form = registration_form))






    #messages.success(request, f'Great news! Your account has been created successfully. We look forward to you using our services!')  