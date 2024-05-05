"""
URL configuration for agentserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'server'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('cmd/', views.get_cmd_res, name='cmd'),
    path('data/', views.make_fake_data, name='fake_data'),
    path('get-data/', views.get_instance_metric, name='get_metrics_data'),
    path('upload-plugin/', views.upload_plugin_page, name='upload_plugin_page_view'),
    path('deploy-host/', views.deploy_host_func, name='deploy_host_func'),
    path('start-host/', views.start_host_func, name='start_host_func'),
    path('stop-host/', views.stop_host_func, name='stop_host'),
    path('del-host/', views.del_host_func, name='del_host'),
    path('host-manage/', views.host_management_page, name='host_manage_page'),
    path('get-host-info/', views.get_deploy_host_info_info, name='get_host_info'),
    path('register-info/', views.register_info_func, name='register_info'),
    path('sync-vm/', views.sync_vm_info_func, name='sync_vn_info'),
    path('v2/sync-cmd/', views.execute_sync_cmd_function, name='execute_sync_cmd'),
    path('install_agent/', views.install_agent, name='install_agent_func'),

]
