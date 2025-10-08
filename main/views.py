from django.shortcuts import render, redirect, get_object_or_404
from main.models import Shop # Asumsi model produk Anda bernama Shop
from main.forms import ShopForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt # Tambahkan ini jika Anda belum menghapusnya

# --- VIEWS UTAMA & CRUD AJAX (Sama seperti sebelumnya) ---

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all") 

    if filter_type == "all":
        product_list = Shop.objects.all()
    else:
        product_list = Shop.objects.filter(user=request.user)

    context = {
        'shop' : "dudushop",
        'name': request.user.username,
        'class': 'PBP B',
        'product_list' : product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html",context)


@login_required(login_url='/login')
def detail_product(request, id):
    product = get_object_or_404(Shop, pk=id)
    return render(request, "detail_product.html", {"product": product})


@login_required(login_url='/login/')
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail_url = request.POST.get('thumbnail_url') 
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on' 

        try:
            price = float(price)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid price format.'}, status=400)
            
        new_product = Shop(
            name=name,
            price=price,
            description=description,
            thumbnail=thumbnail_url,
            category=category,
            is_featured=is_featured,
            user=request.user
        )
        new_product.save()

        return JsonResponse({
            'success': True,
            'message': 'Product added successfully!',
            'product': {
                'id': str(new_product.id),
                'name': new_product.name,
                'price': new_product.price,
                'description': new_product.description,
                'thumbnail': new_product.thumbnail,
                'category': new_product.category,
                'is_featured': new_product.is_featured,
            }
        })
    else:
        return JsonResponse({'success': False, 'detail': 'Method not allowed'}, status=405)


def show_xml(request):
    products_list = Shop.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    products_list = Shop.objects.all() 
    json_data = [
        {
            'pk': product.id, 
            'fields': {
                'name': product.name,
                'price': float(product.price),
                'description': product.description,
                'thumbnail': product.thumbnail if product.thumbnail else "", 
                'category': product.category,
                'is_featured': product.is_featured,
                'user': product.user.username if product.user else None, 
                'user_id': product.user.id if product.user else None,
            }
        }
        for product in products_list
    ]
    return JsonResponse(json_data, safe=False)

def show_xml_by_id(request, news_id):
    try:
        products_item = Shop.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", products_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Shop.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Shop.objects.select_related('user').get(pk=product_id)

        json_data = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'description': product.description,
            'category': product.category, 
            'is_featured': product.is_featured,
            'thumbnail': product.thumbnail if product.thumbnail else "", 
            'user_id': product.user_id,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(json_data)
    except Shop.DoesNotExist:
        return JsonResponse({'detail': 'Product not found'}, status=404)


@login_required(login_url='/login/')
def edit_product_ajax(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Shop, pk=id)

        if product.user != request.user:
            return JsonResponse({'success': False, 'error': 'Not authorized to edit this product.'}, status=403)
            
        name = request.POST.get('name')
        price_str = request.POST.get('price')
        description = request.POST.get('description')
        thumbnail_url = request.POST.get('thumbnail_url')
        category = request.POST.get('category')
        is_featured = request.POST.get('is_featured') == 'on' 
        
        try:
            price = float(price_str)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid price format.'}, status=400)
            
        product.name = name
        product.price = price
        product.description = description
        product.thumbnail = thumbnail_url
        product.category = category
        product.is_featured = is_featured
        
        product.save()

        return JsonResponse({
            'success': True, 
            'message': 'Product updated successfully!',
            'id': str(product.id)
        })
    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)


@login_required(login_url='/login/')
def delete_product(request, id):
    if request.method == 'POST': 
        product = get_object_or_404(Shop, pk=id)

        if product.user != request.user:
            return JsonResponse({'success': False, 'error': 'Not authorized to delete this product.'}, status=403)

        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully.'})

    return JsonResponse({'success': False, 'error': 'Method not allowed.'}, status=405)


# --- VIEWS AUTENTIKASI (DIUBAH KE AJAX) ---

# 1. REGISTER AJAX
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # 💡 Mengembalikan JsonResponse untuk sukses register
            return JsonResponse({'success': True, 'message': 'Akun berhasil dibuat. Silakan login.'}, status=201)
        else:
            # 💡 Mengembalikan JsonResponse dengan error validasi
            errors = dict(form.errors.items())
            return JsonResponse({'success': False, 'errors': errors, 'message': 'Terjadi kesalahan validasi.'}, status=400)
    
    # Tetap mengembalikan form untuk GET request non-ajax, jika dibutuhkan.
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'register.html', context)


# 2. LOGIN AJAX
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # 💡 Mengembalikan JsonResponse, set cookie last_login
            response = JsonResponse({'success': True, 'message': 'Login successful!', 'username': user.username})
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            # 💡 Mengembalikan JsonResponse dengan error (HTTP 400 Bad Request)
            errors = dict(form.errors.items())
            return JsonResponse({'success': False, 'errors': errors, 'message': 'Kredensial tidak valid.'}, status=400)
    
    # Tetap mengembalikan form untuk GET request non-ajax, jika dibutuhkan.
    form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


# 3. LOGOUT AJAX
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        
        # 💡 Mengembalikan JsonResponse dan menghapus cookie
        response = JsonResponse({'success': True, 'message': 'Logout successful!'})
        response.delete_cookie('last_login')
        response.delete_cookie('sessionid')
        return response
        
    # Jika method GET (misalnya diakses langsung dari browser), tetap redirect
    return HttpResponseRedirect(reverse('main:login'))