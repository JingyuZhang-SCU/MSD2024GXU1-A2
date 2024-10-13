# appointment/models.py
from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor_appointments', on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('doctor', 'appointment_time')  # 确保医生在同一时间段只有一个预约
    
    def __str__(self):
        return f"Appointment {self.id} - {self.patient.username} with {self.doctor.username} at {self.appointment_time}"
