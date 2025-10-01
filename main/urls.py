from django.urls import path, include
from main.views import show_main
from main.views import show_main, show_xml, show_json, show_xml_by_id, show_json_by_id, add_product, detail_product
from main.views import register, login_user, logout_user, edit_product, delete_product


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),
    path('product/<str:id>/', detail_product, name='detail_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:news_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:news_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('news/<uuid:id>/edit', edit_product, name='edit_product'),
    path('news/<uuid:id>/delete', delete_product, name='delete_product'),
]