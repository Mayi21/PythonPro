# monitor_web/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('server.urls')),
]