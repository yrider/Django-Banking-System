"""BankingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.urls import path
from .views import HomeView, AboutView, ContactView
from accounts.views import RegisterView, LoginView
from transactions.views import TransactionView, TransferView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name='logout'),
    path('register/', RegisterView.as_view(), name="register"),
    path('transactions/', login_required(TransactionView.as_view()), name="transactions"),
    path('transfers/', login_required(TransferView.as_view()), name="transfers")
]

urlpatterns += staticfiles_urlpatterns()

