# monitor_web/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('api/nodes/', views.node_list, name='node_list'),
    path('api/nodes/<str:node_name>/', views.node_detail, name='node_detail'),
    path('api/execute_command/<str:node_name>/', views.execute_command, name='execute_command'),
    path('api/upload_file/<str:node_name>/', views.upload_file, name='upload_file'),
]