from django.shortcuts import render
from .models import room,storage_device,freeze_shelf,freeze_box,room_storage_relation
from .db import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse, FileResponse
from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from bson.objectid import ObjectId
from .helper import *

# Create your views here.


def query_all_node(request):
    ''' 获取所有节点 '''
    all_room = query_all_room()
    rst = {'store':[]}
    if not all_room:
        first_node = init_node_room()
        rst['store'].append({k:v for k,v in mongo_to_dict_helper(first_node).items()})
    else:
        for room in all_room:
            rst['store'].append({k:v for k,v in mongo_to_dict_helper(room).items()})
            # 查询room下的设备列表
            all_store = query_storage_device_by_room_id(str(room._id))
            for store in all_store:
                rst['store'].append({k:v for k,v in mongo_to_dict_helper(store).items()})
                #查询存储设备里的冻存架
    return JsonResponse(rst)


def add_first_room(request):
    flag = init_node_room() 
    if flag:
        return HttpResponse('初始化成功')
    else:
        return HttpResponse('初始化失败')

def add_new_room(request):
    name = request.POST['name']
    line_order = request.POST['rank']
    parent_id = request.POST['parent_id']
    all_room_ids = query_all_room_ids()
    msg = ''
    if parent_id not in all_room_ids:
         msg = u'父节点不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)

    flag = add_new_room(name, line_order, parent_id)
    if flag:
         rst = {
             'success': flag,
             'code': 200,
             'msg': msg
         }
         return JsonResponse(rst)
    else:
         msg = u'创建失败，数据库错误'
         rst = {
             'success': False,
             'code': 301,
             'msg': msg
         }
         return JsonResponse(rst)


def add_new_storage_device():
    ''' 添加新的设备 '''
    name = request.POST['name']
    line_order = request.POST['rank']
    room_id = request.POST['room_id']
    utype = request.POST['utype']
    all_room_ids = query_all_room_ids()
    msg = ''
    if parent_id not in all_room_ids:
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_storage(name,utype,line_order,room_id)
    if flag:
        rst = {
             'success': flag,
             'code': 200,
             'msg': msg
        }
        return JsonResponse(rst)
    else:
         msg = u'创建失败，数据库错误'
         rst = {
             'success': False,
             'code': 301,
             'msg': msg
         }
         return JsonResponse(rst)
    

def add_new_freeze_shelf():
    ''' 添加新的冻存架 '''
    name = request.POST['name']
    line_order = request.POST['rank']
    shelfline = request.POST['shelfline']     # 行数
    shelfcolumn = request.POST['shelfcolumn'] # 列数
    store_id = request.POST['store_id']       # 存储设备id
    utype = request.POST['utype']             # 冻存架排列方式(1,2,3)
    all_storage_ids = query_all_storage_ids()
    msg = ''
    if store_id not in all_storage_ids :
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_freeze_shelf(shelfname,utype,line_order,store_id,shelfline,shelfcolumn)
    if flag:
        rst = {
             'success': flag,
             'code': 200,
             'msg': msg
        }
        return JsonResponse(rst)
    else:
         msg = u'创建失败，数据库错误'
         rst = {
             'success': False,
             'code': 301,
             'msg': msg
         }
         return JsonResponse(rst)
