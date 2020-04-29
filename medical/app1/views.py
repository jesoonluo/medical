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


def add_new_storage_device(request):
    ''' 添加新的设备 '''
    name = request.POST['name']
    line_order = request.POST['line_order']
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
    

def add_new_freeze_shelf(request):
    ''' 添加新的冻存架 '''
    name = request.POST['name']
    line_order = request.POST['line_order']
    shelfline = request.POST['shelfline']     # 行数
    shelfcolumn = request.POST['shelfcolumn'] # 列数
    store_id = request.POST['storage_id']     # 存储设备id
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


def add_new_freeze_box(request):
    ''' 添加新的冻存盒 '''
    name = request.POST['name']
    line_order = request.POST['line_order']
    boxline = request.POST['boxline']         # 行数
    boxcolumn = request.POST['boxcolumn']     # 列数
    shelf_id = request.POST['shelf_id']       # 冻存架id
    utype = request.POST['utype']             # 冻存盒排列方式(1,2,3)
    msg = ''
    shelf = query_shelf_by_id(shelf_id)
    if not shelf:
         msg = u'冻存架不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    # 获取已经存在的冻存盒数
    boxs = query_boxs_by_shelf_id(shelf_id)
    # TODO根据冻存架type,确定排列位子
    box_order = ''
    if shelf.utype == '1': #1,2,3...,11
        box_order = len(boxs) + 1
    elif shelf.utype == '2':   #11,21,31
        num_shang = len(boxs)//shelf.shelfline
        num_yu = len(boxs)%shelf.shelfline
        if num_yu == 0:
            box_order = str(num_shang+1) + str(1)
        box_order = str(num_shang) + str(num_yu + 1)
    elif shelf.utype == '3':   #11,21,31
        en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I', '10': 'J', '11': 'K', '12': 'L', '13': 'M', '14': 'N'}
        num_shang = len(boxs)//shelf.shelfline
        num_yu = len(boxs)%shelf.shelfline
        if num_yu == 0:
            box_order = en_ch.get(str(num_shang+1)) + str(1)
        box_order = en_ch.get(str(num_shang)) + str(num_yu + 1)
    box_id = request.POST.get('boxid', 'system_add_id')
    box_note = request.POST.get('boxnote', 'system_add_note')
    flag = add_new_freeze_box(name,box_id,utype,box_order,line_order,shelf_id,box_note,boxline,boxcolumn)
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
