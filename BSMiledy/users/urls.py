from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
   path('profile', views.profile, name='profile'),
   path('register', views.RegiserView.as_view(), name='register'),
]