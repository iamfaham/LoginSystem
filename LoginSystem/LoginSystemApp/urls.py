from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('login/', views.loginpage, name='loginpage'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.logoutpage, name = 'logout'),
]