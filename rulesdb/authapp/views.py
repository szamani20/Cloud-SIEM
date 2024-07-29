from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from django.contrib.auth import get_user_model
from logs.models import Log
from notifications.models import Notification, NotificationSubscription
from rules.models import Rule

User = get_user_model()


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('panel')
    else:
        form = SignUpForm()
    return render(request, 'authapp/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel')
    else:
        form = LoginForm()
    return render(request, 'authapp/login.html', {'form': form})


def auth_home_view(request):
    if request.user.is_authenticated:
        return redirect('panel')
    return render(request, 'authapp/auth_home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def panel_view(request):
    return render(request, 'authapp/panel.html')


@login_required
def logs_view(request):
    logs = Log.objects.filter(organization=request.user.organization).order_by('-create_time')
    return render(request, 'authapp/logs.html', {'logs': logs})


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(organization=request.user.organization).order_by('-create_time')
    return render(request, 'authapp/notifications.html', {'notifications': notifications})


@login_required
def notification_subscriptions_view(request):
    notification_subscriptions = NotificationSubscription.objects.filter(organization=request.user.organization).order_by('-create_time')
    return render(request, 'authapp/notification_subscriptions.html', {'notification_subscriptions': notification_subscriptions})


@login_required
def rules_view(request):
    rules = Rule.objects.filter(organization=request.user.organization).order_by('-create_time')
    return render(request, 'authapp/rules.html', {'rules': rules})
