from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, authenticate;
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def userSignin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, "userSignin.html", {'form': form})


def userSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            messages.success(request, 'Registration successful')
            return redirect('userSignin')  # Redirect to home or another appropriate page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()

    return render(request, 'userSignup.html', {'form': form})


def login(request):
    return render(request, "registration/login.html")


def restSignup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("restDashboard.html")
    else:
        form = UserCreationForm()
    return render(request, "registration/restSignup.html", {'form': form})


def restDashboard(request):
    return render(request, "restDashboard.html")


def flavourflow_app(request):
    return render(request, 'index.html')


# @userSignin
def user_dashboard(request):
    return render(request, 'user/dashboard.html')


# def membership(request):
#     pass
def membership(request):
    return render(request, 'membership.html')


@login_required
def home(request):
    return render(request, 'home.html')


def payments(request):
    if request.method == 'POST':
        return render(request, 'payments.html')

    return redirect('payments')


def checkoutOrder(request):

    return render(request, 'checkoutOrder.html')


def checkoutPayment(request):
    return render(request, 'checkoutPayment.html')


def orderTracking(request):
    return render(request, 'orderTracking.html')
