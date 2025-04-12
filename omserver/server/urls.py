# monitor_web/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/install_rpm/', views.deploy_vm, name='deploy_vm'),
    path('api/get_node_info/', views.get_node_info, name='get_node_info'),
    # 确保路径以斜杠结尾
    path('api/task/<str:task_id>/', views.get_task_info, name='get_task_info'),
    path('v2/api/register_node_info', views.update_vm_info, name='update_vm_info'),
    path('v1/api/execute/cmd/', views.exec_shell_command, name='exec_shell_command'),
]