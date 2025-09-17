from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Shop
from main.forms import ShopForm
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    product_list = Shop.objects.all()
    context = {
        'shop' : "dudushop",
        'name' : 'Clairine Christabel Lim',
        'class': 'PBP B',
        'product_list' : product_list
    }

    return render(request, "main.html", context)

def detail_product(request, id):
    product = get_object_or_404(Shop, pk=id)
    return render(request, "detail_product.html", {"product": product})

def add_product(request):
    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:show_main")
    else:
        form = ShopForm()
    return render(request, "add_product.html", {"form": form})

def show_xml(request):
     news_list = Shop.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = Shop.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, news_id):
    try:
        news_item = Shop.objects.filter(pk=news_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Shop.DoesNotExist:
        return HttpResponse(status=404)
   
def show_json_by_id(request, news_id):
    try:
        news_item = Shop.objects.get(pk=news_id)
        json_data = serializers.serialize("json", [news_item])
        return HttpResponse(json_data, content_type="application/json")
    except Shop.DoesNotExist:
        return HttpResponse(status=404)