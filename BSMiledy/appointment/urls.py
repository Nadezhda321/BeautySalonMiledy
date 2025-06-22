from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('create/<int:service_id>/', views.create_appointment, name='create'),
    path('success/', views.appointment_success, name='success'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel'),
]