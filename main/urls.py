from django.urls import path
from main.views import (
    show_main, show_xml, show_json, show_xml_by_id, show_json_by_id, 
    detail_product, register, login_user, logout_user, show_json_by_user,
    edit_product_ajax, delete_product, add_product_ajax, proxy_image, create_product_flutter
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('detail/<uuid:id>/', detail_product, name='detail_product'),
    
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:product_id>/', show_json_by_id, name='show_json_by_id'), 
    
    path('edit-product-ajax/<uuid:id>/', edit_product_ajax, name='edit_product_ajax'),
    path('delete-product/<uuid:id>/', delete_product, name='delete_product'),
    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'),
    
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
    path('json-by-user/', show_json_by_user, name='show_json_by_user'),
]