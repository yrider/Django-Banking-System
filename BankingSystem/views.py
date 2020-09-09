from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import LoginForm, RegisterForm
from .forms import ContactForm
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'accounts/home.html', {'title':'Home'})

class AboutView(View):
    def get(self, request):
        return render(request, 'about_page.html', {'title': 'About'})

class ContactView(TemplateView):
    template_name = 'contact/view.html'
    #success_url = '/'

    def get(self, request):
        form = ContactForm()   
        context = {
            'form':form,
            'title': 'Contact'
        }
        return render(request, 'contact/view.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            #print(form.cleaned_data.get("email"))
            messages.success(request, 'Thank you, your message has been sent. We aim to respond to all messages within 3-5 working days.')
            return redirect('home')
        context = {
            'form':form,
            'title': 'Contact'
        }
        return render(request, 'contact/view.html', context)

