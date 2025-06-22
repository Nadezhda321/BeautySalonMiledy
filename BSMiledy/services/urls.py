from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
   path('', views.services_home, name='services_home'),
   path('gallery/', views.gallery, name='gallery'),
   path('services/<int:service_id>/', views.service_detail, name='service_detail'),
]
