from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
   path('', views.index, name='index'),
   path('politics/', views.politics, name='politics'),
   path('contacts/', views.contacts, name='contacts'),
]
