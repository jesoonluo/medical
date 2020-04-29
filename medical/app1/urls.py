from django.contrib import admin
from django.urls import path
# 导入对应 app 的 views 文件
from . import views

urlpatterns = [
    path('query_node/',views.query_all_node),
    path('add_room/',views.add_new_room),
    path('add_storage_device/',views.add_new_storage_device),
]
