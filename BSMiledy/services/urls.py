from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
   path('', views.services_home, name='services_home'),
]
