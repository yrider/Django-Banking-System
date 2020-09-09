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

from django.contrib import admin
from django.urls import path
from .views import HomeView, AboutView, ContactView
from accounts.views import RegisterView, LoginView, ProfileView
from transactions.views import DepositView, WithdrawalView, LoanView, TransactionView, TransferView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('profile/', login_required(ProfileView.as_view()), name="profile"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name='logout'),
    path('register/', RegisterView.as_view(), name="register"),
    path('deposits/', login_required(DepositView.as_view()), name="deposits"),
    path('withdrawals/', login_required(WithdrawalView.as_view()), name="withdrawals"),
    path('loans/', login_required(LoanView.as_view()), name="loans"),
    path('transactions/', login_required(TransactionView.as_view()), name="transactions"),
    path('transfers/', login_required(TransferView.as_view()), name="transfers")
]

# debug is true during dev but not production. Therefore if below is true static files won't be served as only used for dev phase/testing
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)