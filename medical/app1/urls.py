from django.contrib import admin
from django.urls import path
# 导入对应 app 的 views 文件
from . import views

urlpatterns = [
    path('query_node',views.query_all_node),
    path('query_all',views.query_all_node_new),
    path('query_shelfs',views.query_shelf_by_storage_id),
    path('add_room',views.add_new_room),
    path('delete_unit',views.delete_unit),
    path('update_unit',views.update_unit),
    path('rename_unit',views.rename_unit),
    path('copy_unit',views.copy_unit),
    path('add_storage_device',views.add_new_storage_device),
    path('add_storage_N2',views.add_storage_N2),
    path('add_freeze_shelf',views.add_new_freeze_shelf),
    path('add_freeze_box',views.add_new_freeze_box),
    path('index/',views.index),
]
