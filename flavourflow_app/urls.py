from django.urls import path
from . import views

urlpatterns = [
    path('', views.flavourflow_app, name='flavourflow_app'),
    path('userSignin', views.userSignin, name='userSignin'),
    path('userSignup', views.userSignup, name='userSignup'),
]