import json
from django.shortcuts import render
from .models import room,storage_device,freeze_shelf,freeze_box,room_storage_relation
from .db import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse, FileResponse
from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from bson.objectid import ObjectId
from .helper import *
from django.views.decorators.csrf import csrf_exempt
from mongoengine import connect
# Create your views here.

def query_own_db(func):
    def inner(request,*args,**kwargs):
        #sjkname = json.loads(request.COOKIES.get('dbname'))
        #dbname = 'test1'
        connect(alias='test1_alias',db='test1',host='localhost',port=27017,username='',password='',authentication_source='admin')
        return func(request,*args, **kwargs)
    return inner

def check_login(func):
    def inner(request,*args, **kwargs):
        if request.session.get("uname"):
            return func(request,*args, **kwargs)
        else:
            # 返回登录页面
            return HttpResponseRedirect("/login")
    return inner

def index(request):
    request.META["CSRF_COOKIE_USED"] = False
    return render(request,'index.html')

def test(request):
    return render(request,'test.html')

@csrf_exempt
def delete_unit(request):
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    uid = request.POST.get('uid', '')
    dtype = request.POST.get('dtype', '')
    if not uid:
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf', 'freeze_box'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf', 'freeze_box')"})
    rst = delete_unit_db(uid, dtype, db)
    return JsonResponse(rst)

@csrf_exempt
def update_unit(request):
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    uid = request.POST.get('uid', '')
    new_parent_id = request.POST.get('new_parent_id', '')
    dtype = request.POST.get('dtype', '')
    new_postion = request.POST.get('new_postion', None)
    if dtype == 'freeze_shelf' and (not new_postion):
        return JsonResponse({'success': False, 'code': 201, 'msg': '请指定冻存架位子'})
    if not (uid and new_parent_id):
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid或new_parent_id不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf', 'freeze_box'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf', 'freeze_box')"})
    rst = update_unit_db(uid, new_parent_id , dtype, new_postion, db)
    return JsonResponse(rst)

#@query_own_db
@csrf_exempt
def copy_unit(request):
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    uid = request.POST.get('uid', '')
    new_parent_id = request.POST.get('new_parent_id', '')
    dtype = request.POST.get('dtype', '')
    new_postion = request.POST.get('new_postion', None)
    if dtype == 'freeze_shelf' and (not new_postion):
        return JsonResponse({'success': False, 'code': 201, 'msg': '请指定新冻存架位子'})
    if not (uid and new_parent_id):
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid或new_parent_id不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf', 'freeze_box'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf', 'freeze_box')"})
    rst = copy_unit_view(uid, new_parent_id , dtype, new_postion, db)
    return JsonResponse(rst)

@csrf_exempt
def rename_unit(request):
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    uid = request.POST.get('uid', '')
    new_name = request.POST.get('new_name', '')
    dtype = request.POST.get('dtype', '')
    parent_id = request.POST.get('parent_id', '')
    # 重名检测
    if dtype == 'folder':
        if check_name(new_name, 'room', parent_id, db):
            return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    elif dtype == 'storage':
        if check_name(new_name, 'storage', parent_id, db):
            return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    elif dtype == 'freeze_shelf':
        if check_name(new_name, 'freeze_shelf', parent_id, db):
            return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    elif dtype == 'freeze_box':
        if check_name(new_name, 'freeze_box', parent_id, db):
            return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    if not (uid and new_name):
        return JsonResponse({'success': False, 'code': 201, 'msg': '参数uid或new_name不存在'})
    if not dtype or dtype not in ('folder', 'storage', 'freeze_shelf', 'freeze_box'):
        return JsonResponse({'success': False, 'code': 201, 'msg': "dtype格式不正确,必须为('folder', 'storage', 'freeze_shelf', 'freeze_box')"})
    rst = rename_unit_db(uid, new_name , dtype, db)
    return JsonResponse(rst)

def query_all_node(request):
    ''' 获取所有节点 '''
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    all_room = query_all_room(db)
    rst = {'store':[]}
    if not all_room:
        first_node = init_node_room(db)
        first_room = query_all_room(db)[0]
        uroom = {'dtype': '0'}
        for k,v in first_room.items():
            if k != 'roomtype':
                uroom[k] = v
            else:
                uroom['utype'] = v
        rst['store'].append(uroom)
    else:
        for room in all_room:
            uroom = {'dtype': '0'}
            for k,v in room.items():
                if k != 'roomtype':
                    uroom[k] = v
                else:
                    uroom['utype'] = v
            rst['store'].append(uroom)
            # 查询room下的设备列表
            all_store = query_storage_device_by_room_id(str(room.id), db)
            for store in all_store:
                ustore = {}
                format_list = format_storage_list(store.storagetype , store.storageline, store.storagecolumn, store.detailtype, store.id, 'storage')
                ustore['fridge'] = format_list
                for k,v in store.items():
                    if k not in ('storagetype','detailtype','room_id', 'storagename'):
                        ustore[k] = v
                    elif k == 'storagetype':
                        ustore['utype'] = v
                    elif k == 'storagename':
                        ustore['name'] = v
                    elif k == 'detailtype':
                        ustore['dtype'] = v
                    elif k == 'room_id':
                        ustore['parent_id'] = v
                rst['store'].append(ustore)
    return JsonResponse(rst)

def query_all_node_new(request):
    ''' 获取所有节点 '''
    print('start_init....')
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    import time
    one_time = time.time()
    all_room = query_all_room(db)
    rst = {'store':[]}
    if not all_room:
        first_node = init_node_room(db)
        first_room = query_all_room(db)[0]
        uroom = {'dtype': '0'}
        for k,v in first_room.items():
            if k != 'roomtype':
                uroom[k] = v
            else:
                uroom['utype'] = v
        rst['store'].append(uroom)
    else:
        stores = query_all_storage_device(db)
        for room in all_room:
            uroom = {'dtype': '0'}
            print('init_room....')
            for k,v in room.items():
                if k != 'roomtype':
                    uroom[k] = v
                else:
                    uroom['utype'] = v
            rst['store'].append(uroom)
            # 查询room下的设备列表
            #all_store = query_storage_device_by_room_id(str(room.id), db)
            #stores += all_store
        shelfs = query_all_freeze_shelf(db)
        for store in stores:
            print('init_store....')
            ustore = {}
            format_list = format_storage_list(store.storagetype , store.storageline, store.storagecolumn, store.detailtype, store.id, 'storage', db)
            ustore['fridge'] = format_list
            for k,v in store.items():
                if k not in ('storagetype','detailtype','room_id', 'storagename'):
                    ustore[k] = v
                elif k == 'storagetype':
                    ustore['utype'] = v
                elif k == 'storagename':
                    ustore['name'] = v
                elif k == 'detailtype':
                    ustore['dtype'] = v
                elif k == 'room_id':
                    ustore['parent_id'] = v
            rst['store'].append(ustore)
        boxs = query_all_freeze_box(db)
        print('start_init_shelf....')
        print('shelfs_length:',len(shelfs))
        for shelf in shelfs[:100]:
            foo = {}
            format_list = format_shelf_list(shelf.shelfstyle, shelf.shelftype, shelf.shelfline, shelf.shelfcolumn, shelf.id, db)
            foo['shelf'] = format_list
            for k,v in shelf.items():
                if k not in ('shelftype','detailtype','storageid', 'shelfname'):
                    foo[k] = v
                elif k == 'shelftype':
                    foo['utype'] = v
                elif k == 'shelfname':
                    foo['name'] = v
                elif k == 'detailtype':
                    foo['dtype'] = v
                elif k == 'storageid':
                    foo['parent_id'] = v
            rst['store'].append(foo)
            #查询存储设备里的冻存s
            #all_boxs = query_box_by_shelf_id(str(shelf['id']), db)
            #boxs += all_boxs
        print('start_init_box....')
        print('box_length:',len(boxs))
        for box in boxs[:100]:
            foo = {}
            #format_list = format_box_list(box.boxtype, box.boxline, box.boxcolumn, box.id, db)
            #foo['box'] = format_list
            for k,v in box.items():
                if k not in ('boxtype','shelfid','boxname','detailtype'):
                    foo[k] = v
                elif k == 'boxtype':
                    foo['utype'] = v
                elif k == 'boxname':
                    foo['name'] = v
                elif k == 'detailtype':
                    foo['dtype'] = v
                elif k == 'shelfid':
                    foo['parent_id'] = v
            rst['store'].append(foo)
    print('end_init....')
    two_time = time.time()
    print('用时:', two_time-one_time)
    return JsonResponse(rst)

def query_shelf_by_storage_id(request):
    ''' 获取所有节点 '''
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    storage_id = request.GET['uid']
    freeze_shelfs = query_freeze_shelf_by_store_id(storage_id, db)
    rst = {"shelf": [], 'box_list': []}
    for shelf in freeze_shelfs:
        foo = {}
        format_list = format_shelf_list(shelf.shelfstyle, shelf.shelftype, shelf.shelfline, shelf.shelfcolumn, shelf.id)
        foo['shelf'] = format_list
        for k,v in shelf.items():
            if k not in ('shelftype','detailtype','storageid','shelfname'):
                foo[k] = v
            elif k == 'shelftype':
                foo['utype'] = v
            elif k == 'shelfname':
                foo['name'] = v
            elif k == 'detailtype':
                foo['dtype'] = v
            elif k == 'storageid':
                foo['parent_id'] = v
        rst["shelf"].append(foo)
        #查询存储设备里的冻存架
        boxs = query_box_by_shelf_id(str(shelf.id), db)
        for box in boxs:
            rst['box_list'].append(box)
    return JsonResponse(rst)

def query_shelf_by_storage_id_own(storage_id, db):
    #通过设备id获取冻存架
    rst = []
    freeze_shelfs = query_freeze_shelf_by_store_id(storage_id, db)
    for shelf in freeze_shelfs:
        foo = {}
        format_list = format_shelf_list(shelf.shelfstyle, shelf.shelftype, shelf.shelfline, shelf.shelfcolumn, shelf.id, db)
        foo['shelf'] = format_list
        for k,v in shelf.items():
            if k not in ('shelftype','detailtype','storageid', 'shelfname'):
                foo[k] = v
            elif k == 'shelftype':
                foo['utype'] = v
            elif k == 'shelfname':
                foo['name'] = v
            elif k == 'detailtype':
                foo['dtype'] = v
            elif k == 'storageid':
                foo['parent_id'] = v
        rst.append(foo)
    return rst

def query_box_by_shelf_id(shelf_id, db):
    rst = []
    freeze_boxs = query_boxs_by_shelf_id(shelf_id, db)
    for box in freeze_boxs:
        foo = {}
        format_list = format_box_list(box.boxtype, box.boxline, box.boxcolumn, box.id, db)
        foo['box'] = format_list
        for k,v in box.items():
            if k not in ('boxtype','shelfid','boxname','detailtype'):
                foo[k] = v
            elif k == 'boxtype':
                foo['utype'] = v
            elif k == 'boxname':
                foo['name'] = v
            elif k == 'detailtype':
                foo['dtype'] = v
            elif k == 'shelfid':
                foo['parent_id'] = v
        rst.append(foo)
    return rst

@csrf_exempt
def add_new_room(request):
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    name = request.POST['name']
    parent_id = request.POST['parent_id']
    if check_name(name, 'room', parent_id, db):
        return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    rank = request.POST['rank']
    all_room_ids = query_all_room_ids(db)
    msg = ''
    if parent_id not in all_room_ids:
         msg = u'父节点不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)

    flag = add_room(name, rank, parent_id, db)
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
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    name = request.POST['name']
    room_id = request.POST['parent_id']
    if check_name(name, 'room', room_id, db):
        return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    terminalname = ''
    storageid = request.POST['storage_id']
    rank = request.POST['rank']
    utype = request.POST.get('utype','1')         # 液氮罐编码方式默认为1?
    dtype = request.POST['dtype']
    storageline = 1                               # 冻存架数量
    storagecolumn = request.POST['num']           # 列数 (默认为1)
    all_room_ids = query_all_room_ids(db)
    msg = ''
    if room_id not in all_room_ids:
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_storage(name,terminalname,storageid,utype,dtype,rank,room_id,storageline,storagecolumn,db)
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
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    room_id = request.POST['parent_id']
    name = request.POST['name']
    if check_name(name, 'storage', room_id, db):
        return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    terminalname = request.POST['terminal_name']
    storageid = request.POST['storage_id']
    rank = request.POST['rank']
    utype = request.POST['utype']
    dtype = request.POST['dtype']
    storageline = request.POST['storageline']     # 行数
    storagecolumn = request.POST['storagecolumn'] # 列数
    all_room_ids = query_all_room_ids(db)
    msg = ''
    if room_id not in all_room_ids:
         msg = u'存储空间不存在,请确认'
         rst = {
             'success': False,
             'code': 304,
             'msg': msg
         }
         return JsonResponse(rst)
    flag = add_new_storage(name,terminalname,storageid,utype,dtype,rank,room_id,storageline,storagecolumn,db)
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
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    shelfname = request.POST['name']
    store_id = request.POST['parent_id']      # 存储设备id
    if check_name(shelfname, 'freeze_shelf', store_id, db):
        return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    rank = request.POST['rank']
    shelfline = request.POST['shelfline']     # 行数
    shelfcolumn = request.POST['shelfcolumn'] # 列数
    hands_direction = request.POST['hands_direction']  # 拉手方向
    utype = request.POST['utype']             # 冻存架排列方式(1->正序,2->逆序)
    dtype = request.POST['dtype']             # 冻存架类别
    shelf_order = request.POST['shelf_order'] # 编号,设备上的编号
    shelf_style = request.POST.get('shelf_style','AAA') #冻存架编码方式
    #TODO 验证编号和设备的编码方式是否一致
    msg = ''
    storage = query_storage_by_id(store_id,db)
    if not storage:
        msg = u'存储设备不存在,请确认'
        rst = {
            'success': False,
            'code': 304,
            'msg': msg
        }
        return JsonResponse(rst)
    # 获取已经存在的冻存架数
    #shelfs = query_freeze_shelf_by_store_id(store_id)
    # TODO根据冻存架type,确定排列位子
    # shelf_order = query_code_name_by_type(len(shelfs), storage.utype, storage.storageline, storage.storagecolumn, storage.detailtype )
    flag = add_freeze_shelf(shelfname,utype,dtype,shelf_order,rank,store_id,hands_direction,shelfline,shelfcolumn,db,shelf_style)
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
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    name = request.POST['name']
    shelf_id = request.POST['parent_id']       # 冻存架id
    if check_name(name, 'freeze_box', shelf_id, db):
        return JsonResponse({'success': False, 'code': 301, 'msg': '名字不能重复'})
    rank = request.POST['rank']
    boxline = request.POST['boxline']         # 行数
    boxcolumn = request.POST['boxcolumn']     # 列数
    utype = request.POST['utype']             # 冻存盒排列方式(1,2,3)
    dtype = request.POST['dtype']             # 冻存架类别
    msg = ''
    shelf = query_shelf_by_id(shelf_id,db)
    if not shelf:
        msg = u'冻存架不存在,请确认'
        rst = {
            'success': False,
            'code': 304,
            'msg': msg
        }
        return JsonResponse(rst)
    # 获取已经存在的冻存盒数
    boxs = query_boxs_by_shelf_id(shelf_id,db)
    # TODO根据冻存架type,确定排列位子
    #box_order = query_code_name_by_type(len(boxs), shelf.utype, shelf.shelfline, shelf.shelfcolumn, 'box')
    box_order = request.POST['box_order']
    box_id = request.POST.get('box_id', 'system_add_id')  #自定义id
    box_note = request.POST.get('box_note', 'system_add_note')  # 冻存盒说明
    flag = add_freeze_box(name,box_id,utype,dtype,box_order,rank,shelf_id,box_note,boxline,boxcolumn,db)
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
def add_sample_view(request):
    # cookie 获取db, username, userphone
    db = 'test'
    phone = ''
    username = ''
    data_list = json.loads(request.POST['data_list'])
    if not isinstance(data_list, list):
        msg = u'数据格式解析不正确'
        rst = {
            'success': False,
            'code': 305,
            'msg': msg
        }
        return JsonResponse(rst)

    for item in data_list:
        box_id = item['box_id']
        box = query_freeze_box_by_id(box_id, db)
        if not box:
            msg = u'冻存盒不存在,请确认'
            rst = {
                'success': False,
                'code': 304,
                'msg': msg
            }
            return JsonResponse(rst)
        sample_id = item['sample_id']
        sample_order =  item.get('name', '')
        sample_name = item.get("sample_name", "")
        img_url = item.get("img_url", "")
        add_rst = add_sample(sample_id, box_id, sample_order, db, phone, username, img_url, sample_name)
        if not add_rst:
            msg = u'添加样本失败'
            rst = {
                'success': False,
                'code': 301,
                'msg': msg
            }
            return JsonResponse(rst)
    rst = {
         'success': True,
         'code': 200,
         'msg': ''
    }
    return JsonResponse(rst)

def query_samples(request):
    ''' 获取盒子下所有样本 '''
    # db = json.loads(request.COOKIES.get('dbname'))
    db = 'test'
    box_id = request.GET['box_id']
    samples = query_sample_by_box_id(box_id, db)
    rst = {"samples": samples}
    return JsonResponse(rst)
