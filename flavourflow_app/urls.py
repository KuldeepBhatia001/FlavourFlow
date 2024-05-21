from django.urls import path
from . import views

urlpatterns = [
    path('', views.flavourflow_app, name='flavourflow_app'),
    path('userSignin', views.userSignin, name='userSignin'),
    path('userSignup', views.userSignup, name='userSignup'),
    path('restSignup/', views.restSignup_view, name='restSignup'),
    path('login/', views.login, name='login'),
    path('restDashboard/', views.restDashboard, name='restDashboard'),
    # path('membership/', views.membership, name='membership'),
    path('dashboard/', views.user_dashboard, name='dashboard')

]
