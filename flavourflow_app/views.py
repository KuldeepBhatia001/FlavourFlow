from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm;

def userSignin(request):
    return render(request, "userSignin.html")


def userSignup(request):
    return render(request, "userSignup.html")

def login(request):
    return render(request, "registration/login.html")
    
def restSignup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ("restDashboard.html")
    else:
        form = UserCreationForm()
    return render(request, "registration/restSignup.html", {'form': form})

def restDashboard(request):
    return render(request,"restDashboard.html")

def flavourflow_app(request):
    return render(request, 'index.html')


def membership(request):
    return render(request, 'membership.html')
