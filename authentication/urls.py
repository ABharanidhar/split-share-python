from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login, {'template_name': 'authentication/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/authentication/login'}, name='logout'),
]
