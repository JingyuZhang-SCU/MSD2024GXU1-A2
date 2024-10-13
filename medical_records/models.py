# medical_records/models.py
from django.db import models
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, related_name='medical_records', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor_records', on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Record {self.id} for {self.patient.username}"
