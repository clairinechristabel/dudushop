import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Mengambil data dari request
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        # Cek user
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "status": True,
                    "message": "Login successful!",
                    "username": username,
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Akun dinonaktifkan."
                }, status=401)
        else:
            return JsonResponse({
                "status": False,
                "message": "Username atau password salah."
            }, status=401)
    
    return JsonResponse({"status": False, "message": "Metode tidak diizinkan"}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Mengambil data dari request
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        # Validasi sederhana
        if not username or not password:
             return JsonResponse({"status": False, "message": "Username dan password harus diisi."}, status=400)
        
        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "message": "Username sudah terdaftar."}, status=409)
        
        # Buat user baru
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()

        return JsonResponse({
            "status": True,
            "message": "Registrasi berhasil!",
        }, status=200)

    return JsonResponse({"status": False, "message": "Metode tidak diizinkan"}, status=405)

@csrf_exempt
def logout(request):
    # Input: request
    # Output: JsonResponse
    
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({
            "status": True, 
            "message": "Logout berhasil!"
        }, status=200)
        
    return JsonResponse({
        "status": False, 
        "message": "Metode tidak diizinkan"
    }, status=405)