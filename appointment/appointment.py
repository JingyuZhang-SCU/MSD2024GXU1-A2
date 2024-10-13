# appointment.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime

@csrf_exempt
@login_required
def create_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            doctor_id = data['doctor_id']
            appointment_time = datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M:%S')
            patient = request.user

            # 检查医生是否有冲突的预约
            if Appointment.objects.filter(doctor_id=doctor_id, appointment_time=appointment_time).exists():
                return JsonResponse({'error': '该时间段医生已有预约'}, status=400)
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor_id=doctor_id,
                appointment_time=appointment_time
            )
            return JsonResponse({'message': '预约成功', 'appointment_id': appointment.id}, status=201)
        except KeyError:
            return JsonResponse({'error': '缺少必要字段'}, status=400)
        except ValueError:
            return JsonResponse({'error': '时间格式错误，正确格式为YYYY-MM-DD HH:MM:SS'}, status=400)
    return JsonResponse({'error': '仅支持POST请求'}, status=405)

@login_required
def view_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if request.user.profile.role == 'doctor' and appointment.doctor == request.user or \
           request.user.profile.role == 'patient' and appointment.patient == request.user:
            data = {
                'id': appointment.id,
                'patient_id': appointment.patient.id,
                'doctor_id': appointment.doctor.id,
                'appointment_time': appointment.appointment_time,
                'created_at': appointment.created_at,
                'updated_at': appointment.updated_at,
            }
            return JsonResponse({'appointment': data}, status=200)
        else:
            return JsonResponse({'error': '无权限查看该预约'}, status=403)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': '预约不存在'}, status=404)

@csrf_exempt
@login_required
def cancel_appointment(request, appointment_id):
    if request.method == 'DELETE':
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            if request.user != appointment.patient and request.user.profile.role != 'doctor':
                return JsonResponse({'error': '无权限取消该预约'}, status=403)
            
            appointment.delete()
            return JsonResponse({'message': '预约已取消'}, status=200)
        except Appointment.DoesNotExist:
            return JsonResponse({'error': '预约不存在'}, status=404)
    return JsonResponse({'error': '仅支持DELETE请求'}, status=405)
