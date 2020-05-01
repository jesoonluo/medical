from django.shortcuts import render
from .models import room,storage_device,freeze_shelf,freeze_box,room_storage_relation
from .db import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse, FileResponse
from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from bson.objectid import ObjectId
from .helper import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def check_login(func):
    def inner(request,*args, **kwargs):
        if request.session.get("uname"):
            return func(request,*args, **kwargs)
        else:
            # 返回登录页面
            return HttpResponseRedirect("/login")
    return inner

def index(request):
    return render(request, 'public/index.html')
    
def delete_unit(request):
    uid = request.POST.get('uid', '')
    dtype = request.POST.get('dtype', '')
    if not uid:
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf')"})
    rst = delete_unit(uid, dtype)
    return JsonResponse(rst)

def update_unit(request):
    uid = request.POST.get('uid', '')
    new_parent_id = request.POST.get('new_parent_id', '')
    dtype = request.POST.get('dtype', '')
    if not (uid and new_uid):
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid或new_parent_id不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf')"})
    rst = update_unit(uid, new_parent_id , dtype)
    return JsonResponse(rst)

#@check_login
def query_all_node(request):
    ''' 获取所有节点 '''
    all_room = query_all_room()
    rst = {'store':[]}
    if not all_room:
        first_node = init_node_room()
        rst['store'].append({k:v for k,v in mongo_to_dict_helper(first_node).items()})
    else:
        for room in all_room:
            uroom = {'dtype': '0'}
            for k,v in mongo_to_dict_helper(room).items():
                if k != 'roomtype':
                    uroom[k] = v
                else:
                    uroom['utype'] = v
            rst['store'].append(uroom)
            # 查询room下的设备列表
            all_store = query_storage_device_by_room_id(str(room.id))
            for store in all_store:
                ustore = {}
                format_list = format_storage_list(store.storagetype , store.storageline, store.storagecolumn, store.detailtype, store.id, 'storage')
                ustore['fridge'] = format_list
                for k,v in mongo_to_dict_helper(store).items():
                    if k not in ('storagetype','detailtype','room_id'):
                        ustore[k] = v
                    elif k == 'storagetype':
                        ustore['utype'] = v
                    elif k == 'detailtype':
                        ustore['dtype'] = v
                    elif k == 'room_id':
                        ustore['parent_id'] = v
                rst['store'].append(ustore)
                #查询存储设备里的冻存架
    return JsonResponse(rst)

@csrf_exempt
def add_new_room(request):
    name = request.POST['name']
    rank = request.POST['rank']
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

    flag = add_room(name, rank, parent_id)
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

@csrf_exempt
def add_storage_N2(request):
    ''' 添加液氮罐 '''
    print('*'*10, dict(request.POST))
    name = request.POST['name']
    terminalname = ''
    storageid = request.POST['storage_id']
    rank = request.POST['rank']
    room_id = request.POST['parent_id']
    utype = request.POST.get('utype','1')         # 液氮罐编码方式默认为1?
    dtype = request.POST['dtype']
    storageline = 1                               # 冻存架数量
    storagecolumn = request.POST['num']           # 列数 (默认为1)
    all_room_ids = query_all_room_ids()
    msg = ''
    if room_id not in all_room_ids:
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_storage(name,terminalname,storageid,utype,dtype,rank,room_id,storageline,storagecolumn)
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

@csrf_exempt
def add_new_storage_device(request):
    ''' 添加新的设备 '''
    print('*'*10, dict(request.POST))
    name = request.POST['name']
    terminalname = request.POST['terminal_name']
    storageid = request.POST['storage_id']
    rank = request.POST['rank']
    room_id = request.POST['parent_id']
    utype = request.POST['utype']
    dtype = request.POST['dtype']
    storageline = request.POST['storageline']     # 行数
    storagecolumn = request.POST['storagecolumn'] # 列数
    all_room_ids = query_all_room_ids()
    msg = ''
    if room_id not in all_room_ids:
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_storage(name,terminalname,storageid,utype,dtype,rank,room_id,storageline,storagecolumn)
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
    

@csrf_exempt
def add_new_freeze_shelf(request):
    ''' 添加新的冻存架 '''
    name = request.POST['name']
    rank = request.POST['rank']
    shelfline = request.POST['shelfline']     # 行数
    shelfcolumn = request.POST['shelfcolumn'] # 列数
    store_id = request.POST['parent_id']     # 存储设备id
    utype = request.POST['utype']             # 冻存架排列方式(1,2,3)
    msg = ''
    storage = query_storage_by_id(store_id)
    if not storage:
         msg = u'存储设备不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    # 获取已经存在的冻存架数
    shelfs = query_freeze_shelf_by_store_id(store_id)
    # TODO根据冻存架type,确定排列位子
    shelf_order = query_code_name_by_type(len(shelfs), storage.utype, storage.storageline, storage.storagecolumn, storage.detailtype )
    flag = add_freeze_shelf(shelfname,utype,shelf_order,rank,store_id,shelfline,shelfcolumn)
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


@csrf_exempt
def add_new_freeze_box(request):
    ''' 添加新的冻存盒 '''
    name = request.POST['name']
    rank = request.POST['rank']
    boxline = request.POST['boxline']         # 行数
    boxcolumn = request.POST['boxcolumn']     # 列数
    shelf_id = request.POST['parent_id']       # 冻存架id
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
    box_order = query_code_name_by_type(len(boxs), shelf.utype, shelf.shelfline, shelf.shelfcolumn, 'box')
    box_id = request.POST.get('boxid', 'system_add_id')
    box_note = request.POST.get('boxnote', 'system_add_note')
    flag = add_freeze_box(name,box_id,utype,box_order,rank,shelf_id,box_note,boxline,boxcolumn)
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
