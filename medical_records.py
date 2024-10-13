# medical_records.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MedicalRecord
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@login_required
def create_medical_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient_id = data['patient_id']
            diagnosis = data['diagnosis']
            treatment = data['treatment']
            doctor_id = request.user.id  # 假设登录用户是医生

            record = MedicalRecord.objects.create(
                patient_id=patient_id,
                doctor_id=doctor_id,
                diagnosis=diagnosis,
                treatment=treatment
            )
            return JsonResponse({'message': '医疗记录创建成功', 'record_id': record.id}, status=201)
        except KeyError:
            return JsonResponse({'error': '缺少必要字段'}, status=400)
    return JsonResponse({'error': '仅支持POST请求'}, status=405)

@login_required
def view_medical_record(request, record_id):
    try:
        record = MedicalRecord.objects.get(id=record_id)
        if request.user.profile.role == 'doctor' or record.patient.user == request.user:
            data = {
                'id': record.id,
                'patient_id': record.patient.id,
                'doctor_id': record.doctor.id,
                'diagnosis': record.diagnosis,
                'treatment': record.treatment,
                'created_at': record.created_at,
                'updated_at': record.updated_at,
            }
            return JsonResponse({'record': data}, status=200)
        else:
            return JsonResponse({'error': '无权限查看该记录'}, status=403)
    except MedicalRecord.DoesNotExist:
        return JsonResponse({'error': '医疗记录不存在'}, status=404)

@csrf_exempt
@login_required
def update_medical_record(request, record_id):
    if request.method == 'PUT':
        try:
            record = MedicalRecord.objects.get(id=record_id)
            if request.user.profile.role != 'doctor':
                return JsonResponse({'error': '只有医生可以修改医疗记录'}, status=403)
            
            data = json.loads(request.body)
            record.diagnosis = data.get('diagnosis', record.diagnosis)
            record.treatment = data.get('treatment', record.treatment)
            record.save()
            return JsonResponse({'message': '医疗记录更新成功'}, status=200)
        except MedicalRecord.DoesNotExist:
            return JsonResponse({'error': '医疗记录不存在'}, status=404)
        except KeyError:
            return JsonResponse({'error': '无效的数据'}, status=400)
    return JsonResponse({'error': '仅支持PUT请求'}, status=405)
