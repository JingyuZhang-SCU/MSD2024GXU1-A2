# appointment/urls.py
from django.urls import path
from . import appointment

urlpatterns = [
    path('create/', appointment.create_appointment, name='create_appointment'),
    path('view/<int:appointment_id>/', appointment.view_appointment, name='view_appointment'),
    path('cancel/<int:appointment_id>/', appointment.cancel_appointment, name='cancel_appointment'),
]
