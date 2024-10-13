# medical_records/urls.py
from django.urls import path
from . import medical_records

urlpatterns = [
    path('create/', medical_records.create_medical_record, name='create_medical_record'),
    path('view/<int:record_id>/', medical_records.view_medical_record, name='view_medical_record'),
    path('update/<int:record_id>/', medical_records.update_medical_record, name='update_medical_record'),
]
