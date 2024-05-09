from django.shortcuts import render

def userSignin(request):
    return render(request, "userSignin.html")


def userSignup(request):
    return render(request, "userSignup.html")


def flavourflow_app(request):
    return render(request, 'index.html')
