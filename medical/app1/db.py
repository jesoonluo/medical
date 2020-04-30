from .models import room,storage_device,freeze_shelf,freeze_box,log_info
from bson.objectid import ObjectId

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
    return storage_device.objects.get(store_id)

def query_shelf_by_id(shelf_id):
    return freeze_shelf.objects.get(shelf_id)

def query_boxs_by_shelf_id(shelf_id):
    return freeze_box.objects.filter(shelf_id=shelf_id).all()

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

def add_freeze_shelf(shelfname,utype,shelforder,rank,storage_id,shelfline=10,shelfcolumn=10):
    new_shelf = freeze_shelf(
        shelfname = shelfname,
        shelftype = utype,
        shelforder = shelforder,
        shelfline = shelfline,
        shelfcolumn = shelfcolumn,
        rank = int(rank),
        storageid = storage_id 
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
        shelf_id = shelf_id, 
        box_note=box_note,     # 冻存盒描述
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
