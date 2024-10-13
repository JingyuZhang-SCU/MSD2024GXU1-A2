# auth.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            role = data.get('role', 'patient')  # 默认角色为患者

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '用户名已存在'}, status=400)

            user = User.objects.create_user(username=username, password=password)
            user.profile.role = role  # 假设Profile模型扩展了User模型
            user.profile.save()

            return JsonResponse({'message': '注册成功'}, status=201)
        except KeyError:
            return JsonResponse({'error': '缺少必要字段'}, status=400)
    return JsonResponse({'error': '仅支持POST请求'}, status=405)

@csrf_exempt
def login_user_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': '登录成功'}, status=200)
            else:
                return JsonResponse({'error': '无效的凭证'}, status=401)
        except KeyError:
            return JsonResponse({'error': '缺少必要字段'}, status=400)
    return JsonResponse({'error': '仅支持POST请求'}, status=405)

@csrf_exempt
def logout_user_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': '登出成功'}, status=200)
    return JsonResponse({'error': '仅支持POST请求'}, status=405)
