from .models import room,storage_device,freeze_shelf,freeze_box,log_info
from bson.objectid import ObjectId
import pymongo

mg = pymongo.MongoClient('mongodb://localhost:27017')

class obj(object):
    def __init__(self, d):
        self.my_d = d
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            elif a == '_id':
                setattr(self, 'id', str(b))
                setattr(self, '_id', str(b))
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)
    def items(self):
        my_d = self.my_d
        my_d['id'] = str(my_d['_id'])
        my_d['_id'] = str(my_d['_id'])
        return my_d.items()
        

def _query(collection, query, db=None):
    return [obj(i) for i in mg[db][collection].find(query) if i]


def _insert_one(collection, data, db=None):
    return mg[db][collection].insert_one(data).inserted_id


def _insert_many(collection, data, db=None):
    if not data:
        return 0
    return mg[db][collection].insert_many(data).inserted_ids


def _delete_by_id(collection, _id, db):
    return mg[db][collection].delete_one({'_id': ObjectId(_id)}).deleted_count


def _update_one(collection, _filter, data, db=None):
    return mg[db][collection].update_one(_filter, {'$set': data})


def _update_by_id(collection, _id, data, db=None):
    return _update_one(collection, {'_id': ObjectId(_id)}, data, db)


def _find_all(collection, query={}, db=None):
    return [obj(i) for i in mg[db][collection].find(query) if i]

def _find_by_id(collection, _id, db=None):
    item = mg[db][collection].find_one({'_id': ObjectId(_id)})
    return obj(item) if item else None

def _find_one(collection, _filter, db=None):
    item = mg[db][collection].find_one(_filter)
    return obj(item) if item else None

def query_all_room(db):
    return _find_all('room', {}, db)

def query_all_room_ids(db):
    return [str(i._id) for i in _find_all('room', {}, db)]

def query_all_storage_ids(db):
    return [str(i._id) for i in _find_all('storage_device', {}, db)]

def query_storage_device_by_room_id(room_id, db):
    return _query('storage_device', {'room_id': room_id}, db)

def query_freeze_shelf_by_store_id(store_id, db):
    return _query('freeze_shelf', {'storageid': store_id}, db)

def query_storage_by_id(store_id, db):
    return _find_by_id('storage_device', store_id, db)

def query_shelf_by_id(shelf_id, db):
    return _find_by_id('freeze_shelf', shelf_id, db)

def query_boxs_by_shelf_id(shelf_id, db):
    return _query('freeze_box', {'shelfid': shelf_id}, db)

def _insert_log(db, table, op_type, op_id, desc_id='', desc_text=''):
    data = {"operate_table": table, "operate_type": op_type, "operate_id": str(op_id), "operate_desc": desc_text, "destination_id": desc_id}
    try:
        _insert_one('log_info', data, db)
    except:
        return False
    return True

def check_name(new_name, dtype, parent_id, db):
    obj = None
    if dtype == 'room':
        obj = _find_one('room', {'parent_id': parent_id, "name": new_name}, db)
    elif dtype == 'storage':
        obj = _find_one('storage_device', {'room_id': parent_id, "storagename": new_name}, db)
    elif dtype == 'freeze_shelf':
        obj = _find_one('freeze_shelf', {'storageid': parent_id, "shelfname": new_name}, db)
    elif dtype == 'freeze_box':
        obj = _find_one('freeze_box', {'shelfid': parent_id, "boxname": new_name}, db)
    if obj:
        return True
    return False

def init_node_room(db):
    exist = _find_one('room', {'parent_id': '0'}, db)
    if exist:
        return exist
    data = dict(
        name = '全部空间',
        rank = 1,                   #层级
        parent_id = '0'                   #根节点
    )
    insert_id = ""
    try:
        insert_id = _insert_one('room', data, db)
        log = _insert_log(db, 'room', 'add', str(new_first_node.id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return insert_id

def rename_unit_db(uid, new_name, dtype, db):
    #判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        new_room = _find_by_id('room', uid, db)
        if not new_room:
             return {'success': False, 'msg': u'空间不存在', 'code': 302}
        try:
            _update_by_id('room', uid, {'name': new_name}, db)
            log = _insert_log(db, 'room', 'update', str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        store = _find_by_id('storage_device', uid, db)
        if not store:
             return {'success': False, 'msg': u'设备不存在', 'code': 302}
        try:
            _update_by_id('storage_device', uid, {'storagename': new_name}, db)
            log = _insert_log(db, 'storage_device', 'update', str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        shelf = _find_by_id('freeze_shelf', uid, db)
        if not shelf:
             return {'success': False, 'msg': u'冻存架不存在', 'code': 302}
        try:
            _update_by_id('freeze_shelf', uid, {'shelfname': new_name}, db)
            log = _insert_log(db, 'freeze_shelf', 'update', str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            _update_by_id('freeze_box', uid, {'boxname': new_name}, db)
            log = _insert_log(db, 'freeze_box', 'update', str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}

def delete_unit_db(uid, dtype, db):
    #判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        child_room = _find_all("room", {"parent_id": uid}, db)
        child_storage = _find_all("storage_device", {"room_id": uid}, db)
        if child_room or child_storage:
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            _delete_by_id('room', uid, db)
            log = _insert_log(db, 'room', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        store = _find_by_id('storage_device', uid, db)
        child_shelf = _find_all("freeze_shelf", {"storageid": uid}, db)
        if child_shelf or (not store):
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            _delete_by_id('storage_device', uid, db)
            log = _insert_log(db, 'storage_device', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        shelf = _find_by_id('freeze_shelf', uid, db)
        child_shelf = _find_all("freeze_box", {"shelfid": uid}, db)
        if child_shelf or (not shelf):
             return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            _delete_by_id('freeze_shelf', uid, db)
            log = _insert_log(db, 'freeze_shelf', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            _delete_by_id('freeze_box', uid, db)
            log = _insert_log(db, 'freeze_box', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}

def update_unit_db(uid, new_parent_id, dtype, new_position=None, db=None):
    #判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        uparent = _find_by_id('room', new_parent_id, db)
        if not uparent:
             return {'success': False, 'msg': u'新父节点不存在', 'code': 302}
        try:
            _update_by_id('room', uid, {"parent_id": new_parent_id}, db)
            log = _insert_log(db, 'room', 'update', str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        uroom = _find_by_id('room', new_parent_id, db)
        if not uroom:
             return {'success': False, 'msg': u'空间不存在', 'code': 302}
        try:
            _update_by_id('storage_device', uid, {"room_id": new_parent_id}, db)
            log = _insert_log(db, 'storage_device', 'update', str(uid), str(new_parent_id))
        except:
            return {'success': True, 'msg': u'', 'code':200}
        return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        ustorage = _find_by_id('storage_device', new_parent_id, db)
        if not ustorage or (not new_position):
            return {'success': False, 'msg': u'设备不存在或是未指定位子', 'code': 302}
        try:
            _update_by_id('freeze_shelf', uid, {"storageid": new_parent_id, "shelforder": new_position}, db)
            log = _insert_log(db, 'freeze_shelf', 'update', str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            _update_by_id('freeze_box', uid, {"shelfid": new_parent_id, "boxorder": new_position}, db)
            log = _insert_log(db, 'freeze_box', 'update', str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code':200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}

def _copy_name(old_name):
    new_name = old_name
    if old_name.endswith(")"):
        try:
            order = int(old_name[-2])
            new_order = order + 1
            new_name = old_name.split('(')[0] + '(' + str(new_order) + ')'
        except:
            new_name = old_name + '(1)'
    else:
        new_name = old_name + '(1)'
    return new_name

def is_exist_name_by_table_parent_id(table, parent_id, name, db):
    name_list = []
    if table == 'room':
        room_objs = _find_all("room", {"parent_id": parent_id}, db)
        name_list = [i.name for i in room_objs]    
    elif table == 'storage':
        store_objs = _find_all("storage_device", {"room_id": parent_id}, db)
        name_list = [i.storagename for i in store_objs]    
    elif table == 'shelf':
        shelf_objs = _find_all("freeze_shelf", {"storageid": parent_id}, db)
        name_list = [i.shelfname for i in shelf_objs]    
    elif table == 'box':
        box_objs = _find_all("freeze_box", {"shelfid": parent_id}, db)
        name_list = [i.boxname for i in box_objs]    
    if name in name_list:
        return True
    else:
        return False
        
def _copy_unit(obj, table, parent_id, db=None, new_position=None):
    new_id = None
    if table == 'room':
        new_name = obj.name
        if is_exist_name_by_table_parent_id(table, parent_id, obj.name, db):
            new_name = _copy_name(obj.name)
        new_id = add_room(new_name, obj.rank, parent_id, db)
    elif table == 'storage':
        new_name = obj.storagename
        if is_exist_name_by_table_parent_id(table, parent_id, obj.storagename, db):
            new_name = _copy_name(obj.storagename)
        new_id = add_new_storage(
            new_name,
            obj.terminalname,
            obj.storageid,
            obj.storagetype,
            obj.detailtype,
            obj.rank,
            parent_id, 
            obj.storageline, 
            obj.storagecolumn,
            db
        )
    elif table == 'shelf':
        new_name = obj.shelfname
        if is_exist_name_by_table_parent_id(table, parent_id, obj.shelfname, db):
            new_name = _copy_name(obj.shelfname)
        new_id = add_freeze_shelf(
            new_name,
            obj.shelftype,
            obj.detailtype,
            new_position if new_position else obj.shelforder,
            obj.rank,
            parent_id,
            obj.hands_direction,
            obj.shelfline,
            obj.shelfcolumn,
            db
        )
    elif table == 'box':
        new_name = obj.boxname
        if is_exist_name_by_table_parent_id(table, parent_id, obj.boxname, db):
            new_name = _copy_name(obj.boxname)
        new_id = add_freeze_box(
            new_name,
            obj.boxid,
            obj.boxtype,
            obj.detailtype,
            new_position if new_position else obj.boxorder,
            obj.rank,
            parent_id,
            obj.boxnote,
            obj.boxline,
            obj.boxcolumn,
            db
        )
    return new_id

def copy_unit_view(uid, new_parent_id, dtype, new_postion, db):
    #try:
    if dtype == 'folder':
        uparent = room.objects.filter(id=new_parent_id).first()
        if not uparent:
             return {'success': False, 'msg': u'新父节点不存在', 'code': 302}
        old_room = _find_by_id('room', uid, db)
        new_room_id = _copy_unit(old_room,'room', str(room.parent_id), db)
        # 复制room下冰箱
        stores = query_storage_device_by_room_id(str(room.id), db)
        for store in stores:
            new_store_id = _copy_unit(store,'storage', new_room_id, db)
            # 复制设备下冻存架
            shelfs = query_freeze_shelf_by_store_id(str(store.id), db)
            for shelf in shelfs:
                new_shelf_id = _copy_unit(shelf,'shelf', new_store_id, db)
                # 复制冻存架下面冻存盒
                boxs = query_boxs_by_shelf_id(str(shelf.id), db)
                for box in boxs:
                    new_box_id = _copy_unit(box,'box', new_shelf_id, db)
    elif dtype == 'storage':
        uroom = _find_by_id('room', new_parent_id, db)
        if not uroom:
             return {'success': False, 'msg': u'空间不存在', 'code': 302}
        store = _find_by_id('storage_device', uid, db)
        new_store_id = _copy_unit(store,'storage', new_parent_id, db)
        # 复制设备下冻存架
        shelfs = query_freeze_shelf_by_store_id(str(store.id), db)
        for shelf in shelfs:
            new_shelf_id = _copy_unit(shelf,'shelf', new_store_id, db)
            # 复制冻存架下面冻存盒
            boxs = query_boxs_by_shelf_id(str(shelf.id), db)
            for box in boxs:
                new_box_id = _copy_unit(box,'box', new_shelf_id, db)
    elif dtype == 'freeze_shelf':
        ustorage = _find_by_id('storage_device', new_parent_id, db)
        if not ustorage:
             return {'success': False, 'msg': u'设备不存在', 'code': 302}
        shelf = _find_by_id('freeze_shelf', uid, db)
        new_shelf_id = _copy_unit(shelf,'shelf', new_parent_id, db, new_postion)
        boxs = query_boxs_by_shelf_id(uid, db)
        for box in boxs:
            new_box_id = _copy_unit(box, 'box', new_shelf_id, db)
    elif dtype == 'freeze_box':
        shelf = _find_by_id('freeze_shelf', new_parent_id, db)
        if not shelf:
             return {'success': False, 'msg': u'冻存架不存在', 'code': 302}
        box = _find_by_id('freeze_box', uid, db)
        new_box = _copy_unit(box,'box', new_parent_id, db, new_postion)
    return {'success': True, 'msg': u'', 'code':200}
    #except:
    #   return {'success': False, 'msg': u'复制失败,数据库错误', 'code': 301}

def add_room(name, rank, parent_id, db):
    data = dict(
        name = name,
        rank = int(rank),                 #层级
        parent_id = parent_id,
        roomtype = 'folder'
    )
    insert_id = ""
    try:
        insert_id = _insert_one('room', data, db)
        log = _insert_log(db, 'room', 'add', str(insert_id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(insert_id)

def add_new_storage(storagename,terminalname,storageid,utype,dtype,rank,room_id, storageline=10, storagecolumn=10,db=None):
    data = dict(
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
    insert_id = ""
    try:
        insert_id = _insert_one('storage_device', data, db)
        log = _insert_log(db, 'storage_device', 'add', str(insert_id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(insert_id)

def add_freeze_shelf(shelfname,utype,dtype,shelforder,rank,storage_id,hands_direction,shelfline=10,shelfcolumn=10,db=None,shelf_style='AAA'):
    data = dict(
        shelfname = shelfname,
        shelftype = utype,
        detailtype = dtype,
        shelforder = shelforder,
        shelfline = shelfline,
        shelfcolumn = shelfcolumn,
        rank = int(rank),
        storageid = storage_id,
        hands_direction=hands_direction,
        shelfstyle=shelf_style
    )
    try:
        insert_id = _insert_one('freeze_shelf', data, db)
        log = _insert_log(db, 'freeze_shelf', 'add', str(insert_id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(insert_id)

def add_freeze_box(boxname,boxid,utype,dtype,boxorder,rank,shelf_id,box_note,boxline=10,boxcolumn=10,db=None):
    data = dict(
        boxname = boxname,
        boxid = boxid,         # 冻存盒自定义id
        boxorder = boxorder,   # 根据冻存架的类别确定1,11,A1
        boxtype = utype,
        detailtype = dtype,
        boxline = boxline,
        boxcolumn = boxcolumn,
        rank = int(rank),
        shelfid = shelf_id, 
        boxnote=box_note,     # 冻存盒描述
    )
    try:
        insert_id = _insert_one('freeze_box', data, db)
        log = _insert_log(db, 'freeze_box', 'add', str(insert_id))
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(insert_id)

def query_item_by_code_by_id(utable, parent_id, code_name, db):
    if utable == 'storage':
        rst = _query('freeze_shelf', {'storageid': parent_id, 'shelforder': str(code_name)}, db)
        return rst[0] if rst else None
    elif utable == 'shelf':
        rst = _query('freeze_box', {'shelfid': parent_id, 'boxorder': str(code_name)}, db)
        return rst[0] if rst else None
