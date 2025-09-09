from django.urls import path, include
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', include('main.urls')),
    path('', show_main, name='show_main')
]