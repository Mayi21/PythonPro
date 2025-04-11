# monitor_web/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/nodes/', views.node_list, name='node_list'),
    path('api/nodes/<str:node_name>/', views.node_detail, name='node_detail'),
    path('api/execute_command/<str:node_name>/', views.execute_command, name='execute_command'),
    path('api/upload_file/<str:node_name>/', views.upload_file, name='upload_file'),
    path('api/install_rpm/', views.deploy_vm, name='deploy_vm'),
    path('api/task/<str:task_id>', views.get_task_info, name='get_task_info'),
    path('v2/api/register_node_info', views.update_vm_info, name='upload_file'),
]