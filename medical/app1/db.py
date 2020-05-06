from .models import room,storage_device,freeze_shelf,freeze_box,log_info
from bson.objectid import ObjectId

def query_all_room():
    return room.objects.all()

def query_all_room_ids():
    return [str(i.id) for i in room.objects.all()]

def query_all_storage_ids():
    return [str(i.id) for i in storage_device.objects.all()]

def query_storage_device_by_room_id(room_id):
    return storage_device.objects.filter(room_id=room_id).all()

def query_freeze_shelf_by_store_id(store_id):
    return freeze_shelf.objects.filter(storageid =store_id).all()

def query_storage_by_id(store_id):
    return storage_device.objects.filter(id=store_id).first()

def query_shelf_by_id(shelf_id):
    return freeze_shelf.objects.filter(id=shelf_id).first()

def query_boxs_by_shelf_id(shelf_id):
    return freeze_box.objects.filter(shelfid=shelf_id).all()

def _insert_log(table, op_type, op_id, desc_id='', desc_text=''):
    log = log_info.objects.create(
        operate_table = table,
        operate_type = op_type,
        operate_id = str(op_id),
        operate_desc = desc_text,
        destination_id = desc_id
    )
    try:
        log.save()
    except:
        return False
    return True

def init_node_room():
    exist = room.objects.filter(parent_id='0').first()
    if exist:
        return exist
    new_first_node = room.objects.create(
        name = '全部空间',
        rank = 1,                   #层级
        parent_id = '0'                   #根节点
    )
    try:
        new_first_node.save()
        log = _insert_log('room', 'add', str(new_first_node.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return new_first_node

def delete_unit_db(uid, dtype):
    #判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        child_room = room.objects.filter(parent_id=uid).all()
        child_storage = storage_device.objects.filter(room_id=uid).all()
        if child_room or child_storage:
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            room.objects.filter(id=uid).delete()
            log = _insert_log('room', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        child_shelf = freeze_shelf.objects.filter(storageid=uid).all()
        if child_shelf:
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            storage_device.objects.filter(id=uid).delete()
            log = _insert_log('storage_device', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        child_shelf = freeze_box.objects.filter(shelfid=uid).all()
        if child_shelf:
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            freeze_shelf.objects.filter(id=uid).delete()
            log = _insert_log('freeze_shelf', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}

def update_unit_db(uid, new_parent_id, dtype):
    #判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        uparent = room.objects.filter(id=new_parent_id).first()
        if not uparent:
             return {'success': False, 'msg': u'新父节点不存在', 'code': 302}
        try:
            room.objects(id=uid).update(parent_id=new_parent_id)
            log = _insert_log('room', 'update', str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        uroom = room.objects.filter(id=new_parent_id).first()
        if not uroom:
             return {'success': False, 'msg': u'空间不存在', 'code': 302}
        storage_device.objects(id=uid).update(room_id=new_parent_id)
        log = _insert_log('storage_device', 'update', str(uid), str(new_parent_id))
        return {'success': True, 'msg': u'', 'code':200}
        #return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        ustorage = storage_device.objects.filter(id=new_parent_id).first()
        if not ustorage:
             return {'success': False, 'msg': u'设备不存在', 'code': 302}
        try:
            shelf_obj.objects(id=uid).update({"storageid": new_parent_id})
            log = _insert_log('freeze_shelf', 'update', str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}

def delete_storage():
    pass

def add_room(name, rank, parent_id):
    new_node = room.objects.create(
        name = name,
        rank = int(rank),
        parent_id = parent_id                  
    )
    try:
        new_node.save()
        log = _insert_log('room', 'add', str(new_node.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(new_node.id)

def add_new_storage(storagename,terminalname,storageid,utype,dtype,rank,room_id, storageline=10, storagecolumn=10):
    new_store = storage_device(
        storagename = storagename,
        terminalname = terminalname,
        storageid = storageid,  # 设备自定义id
        storagetype = utype,
        detailtype = dtype,
        storageline = storageline,
        storagecolumn = storagecolumn,
        rank = int(rank),
        room_id = room_id
    )
    try:
        new_store.save()
        log = _insert_log('storage_device', 'add', str(new_store.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(new_store.id)

def add_freeze_shelf(shelfname,utype,dtype,shelforder,rank,storage_id,hands_direction,shelfline=10,shelfcolumn=10):
    new_shelf = freeze_shelf(
        shelfname = shelfname,
        shelftype = utype,
        detailtype = dtype,
        shelforder = shelforder,
        shelfline = shelfline,
        shelfcolumn = shelfcolumn,
        rank = int(rank),
        storageid = storage_id,
        hands_direction=hands_direction
    )
    try:
        new_shelf.save()
        log = _insert_log('freeze_shelf', 'add', str(new_shelf.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(new_shelf.id)

def add_freeze_box(boxname,boxid,utype,boxorder,rank,shelf_id,box_note,boxline=10,boxcolumn=10):
    new_box = freeze_box(
        boxname = boxname,
        boxid = boxid,         # 冻存盒自定义id
        boxorder = boxorder,   # 根据冻存架的类别确定1,11,A1
        boxtype = utype,
        boxline = boxline,
        boxcolumn = boxcolumn,
        rank = int(rank),
        shelfid = shelf_id, 
        boxnote=box_note,     # 冻存盒描述
    )
    try:
        new_box.save()
        log = _insert_log('freeze_box', 'add', str(new_box.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(new_box.id)

def query_item_by_code_by_id(utable, parent_id, code_name):
    if utable == 'storage':
        return freeze_shelf.objects.filter(storageid=parent_id).filter(shelforder=code_name).first()
    elif utable == 'shelf':
        return freeze_box.objects.filter(shelfid=parent_id).filter(boxorder=code_name).first()
