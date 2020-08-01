from .models import room, storage_device, freeze_shelf, freeze_box, log_info
from bson.objectid import ObjectId
import pymongo
import pytz
import json
from datetime import datetime
import json

mg = pymongo.MongoClient('mongodb://localhost:27017')


class obj(object):
    def __init__(self, d):
        self.my_d = d
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(
                    x, dict) else x for x in b])
            elif a == '_id':
                setattr(self, 'id', str(b))
                setattr(self, '_id', str(b))
            else:
                setattr(self, a, b if isinstance(b, dict) else b)

    def items(self):
        my_d = self.my_d
        my_d['id'] = str(my_d['_id'])
        del my_d['_id']
        return my_d.items()


def now_ts(lite=False):
    if lite:
        return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
    return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')


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
    return [obj(i) for i in mg[db][collection].find(query)]


def _find_by_id(collection, _id, db=None):
    item = mg[db][collection].find_one({'_id': ObjectId(_id)})
    return obj(item) if item else None


def _find_one(collection, _filter, db=None):
    item = mg[db][collection].find_one(_filter)
    return obj(item) if item else None


def query_all_room(db):
    return _find_all('room', {}, db)

def query_all_storage_device(db):
    return _find_all('storage_device', {}, db)

def query_all_freeze_shelf(db):
    return _find_all('freeze_shelf', {}, db)

def query_all_freeze_box(db):
    return _find_all('freeze_box', {}, db)

def query_all_room_ids(db):
    return [str(i._id) for i in _find_all('room', {}, db)]

def query_all_storage_ids(db):
    return [str(i._id) for i in _find_all('storage_device', {}, db)]


def query_storage_device_by_room_id(room_id, db):
    return _query('storage_device', {'room_id': room_id}, db)


def query_freeze_shelf_by_store_id(store_id, db):
    return _query('freeze_shelf', {'storageid': store_id}, db)


def query_freeze_box_by_id(box_id, db):
    return _find_by_id('freeze_box', box_id, db)


def query_storage_by_id(store_id, db):
    return _find_by_id('storage_device', store_id, db)


def query_shelf_by_id(shelf_id, db):
    return _find_by_id('freeze_shelf', shelf_id, db)


def query_boxs_by_shelf_id(shelf_id, db):
    return _query('freeze_box', {'shelfid': shelf_id}, db)

def query_samples_by_box_id(box_id, db):
    return _find_all('level3mp', {'box_id': str(box_id)}, db)

def _insert_log(db, table, op_type, op_id, desc_id='', desc_text=''):
    data = {
        "operate_table": table,
        "operate_type": op_type,
        "operate_id": str(op_id),
        "operate_desc": desc_text,
        "destination_id": desc_id,
        "dt_create": now_ts()
    }
    try:
        _insert_one('log_info', data, db)
    except:
        return False
    return True


def _insert_sample_log(db, sample_id, sample_define_id, old_box_id, old_order, old_shelf_id, old_storage_id, new_box_id,
                       new_order, new_shelf_id, new_storage_id, op_user_phone, op_user_name, op_type=""):
    data = {
        "old_box_id": str(old_box_id),
        "old_order": old_order,
        "old_shelf_id_": str(old_shelf_id),
        "old_storage_id_": str(old_storage_id),
        "new_box_id": str(new_box_id),
        "new_order": new_order,
        "new_shelf_id_": str(new_shelf_id),
        "new_storage_id_": str(new_storage_id),
        "sample_id": sample_id,
        "sample_define_id": sample_define_id,
        "op_user_phone": op_user_phone,
        "op_user_name": op_user_name,
        "op_type": op_type,
        "dt_create": now_ts()
    }
    try:
        _insert_one('sample_log', data, db)
    except:
        return False
    return True


def check_name(new_name, dtype, parent_id, db):
    obj = None
    if dtype == 'room':
        obj = _find_one('room', {'parent_id': parent_id, "name": new_name}, db)
    elif dtype == 'storage':
        obj = _find_one('storage_device', {
                        'room_id': parent_id, "storagename": new_name}, db)
    elif dtype == 'freeze_shelf':
        obj = _find_one('freeze_shelf', {
                        'storageid': parent_id, "shelfname": new_name}, db)
    elif dtype == 'freeze_box':
        obj = _find_one(
            'freeze_box', {'shelfid': parent_id, "boxname": new_name}, db)
    if obj:
        return True
    return False


def init_node_room(db):
    exist = _find_one('room', {'parent_id': '0'}, db)
    if exist:
        return exist
    data = dict(
        name='全部空间',
        rank=1,  # 层级
        parent_id='0',  # 根节点
        roomtype='folder'
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
    # 判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        new_room = _find_by_id('room', uid, db)
        if not new_room:
            return {'success': False, 'msg': u'空间不存在', 'code': 302}
        try:
            _update_by_id('room', uid, {'name': new_name}, db)
            log = _insert_log(db, 'room', 'update', str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        store = _find_by_id('storage_device', uid, db)
        if not store:
            return {'success': False, 'msg': u'设备不存在', 'code': 302}
        try:
            _update_by_id('storage_device', uid, {'storagename': new_name}, db)
            log = _insert_log(db, 'storage_device', 'update',
                              str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        shelf = _find_by_id('freeze_shelf', uid, db)
        if not shelf:
            return {'success': False, 'msg': u'冻存架不存在', 'code': 302}
        try:
            _update_by_id('freeze_shelf', uid, {'shelfname': new_name}, db)
            log = _insert_log(db, 'freeze_shelf', 'update',
                              str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            _update_by_id('freeze_box', uid, {'boxname': new_name}, db)
            log = _insert_log(db, 'freeze_box', 'update',
                              str(uid), 'update_name')
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'更新失败,数据库错误', 'code': 301}


def delete_unit_db(uid, dtype, db):
    # 判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        child_room = _find_all("room", {"parent_id": uid}, db)
        child_storage = _find_all("storage_device", {"room_id": uid}, db)
        if child_room or child_storage:
            return {'success': False, 'msg': u'该空间下存在未删除子集', 'code': 302}
        try:
            _delete_by_id('room', uid, db)
            log = _insert_log(db, 'room', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code': 200}
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
            return {'success': True, 'msg': u'', 'code': 200}
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
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            _delete_by_id('freeze_box', uid, db)
            log = _insert_log(db, 'freeze_box', 'delete', str(uid))
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'删除失败,数据库错误', 'code': 301}


def update_unit_db(uid, new_parent_id, dtype, new_position=None, db=None, op_user='', op_phone=''):
    # 判断该room下是否存在别的空间或是存储设备
    if dtype == 'folder':
        uparent = _find_by_id('room', new_parent_id, db)
        if not uparent:
            return {'success': False, 'msg': u'新父节点不存在', 'code': 302}
        try:
            _update_by_id('room', uid, {"parent_id": new_parent_id}, db)
            log = _insert_log(db, 'room', 'update',
                              str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'storage':
        uroom = _find_by_id('room', new_parent_id, db)
        if not uroom:
            return {'success': False, 'msg': u'空间不存在', 'code': 302}
        try:
            _update_by_id('storage_device', uid, {
                          "room_id": new_parent_id}, db)
            log = _insert_log(db, 'storage_device', 'update',
                              str(uid), str(new_parent_id))
        except:
            return {'success': True, 'msg': u'', 'code': 200}
        return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_shelf':
        ustorage = _find_by_id('storage_device', new_parent_id, db)
        if not ustorage or (not new_position):
            return {'success': False, 'msg': u'设备不存在或是未指定位子', 'code': 302}
        try:
            # TODO 样本位子迁移日志记录
            add_sample_log_cut_shelf(uid, new_parent_id, op_user, op_phone, db)
            _update_by_id('freeze_shelf', uid, {
                          "storageid": new_parent_id, "shelforder": new_position}, db)
            log = _insert_log(db, 'freeze_shelf', 'update',
                              str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code': 200}
        except:
            return {'success': False, 'msg': u'迁移失败,数据库错误', 'code': 301}
    elif dtype == 'freeze_box':
        try:
            # TODO 样本位子迁移日志记录
            add_sample_log_cut_box(uid, new_parent_id, op_user, op_phone, db)
            _update_by_id('freeze_box', uid, {
                          "shelfid": new_parent_id, "boxorder": new_position}, db)
            log = _insert_log(db, 'freeze_box', 'update',
                              str(uid), str(new_parent_id))
            return {'success': True, 'msg': u'', 'code': 200}
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
        new_storageid = query_uid_by_type(db, table)
        new_name = obj.storagename
        if is_exist_name_by_table_parent_id(table, parent_id, obj.storagename, db):
            new_name = _copy_name(obj.storagename)
        new_id = add_new_storage(
            new_name,
            obj.terminalname,
            new_storageid,
            obj.storagetype,
            obj.detailtype,
            obj.rank,
            parent_id,
            obj.storageline,
            obj.storagecolumn,
            db
        )
    elif table == 'shelf':
        new_shelfid = query_uid_by_type(db, table)
        new_name = obj.shelfname
        if is_exist_name_by_table_parent_id(table, parent_id, obj.shelfname, db):
            new_name = _copy_name(obj.shelfname)
        new_id = add_freeze_shelf(
            new_name,
            obj.shelftype,
            obj.detailtype,
            new_shelfid,
            new_position if new_position else obj.shelforder,
            obj.rank,
            parent_id,
            obj.hands_direction,
            obj.shelfline,
            obj.shelfcolumn,
            db
        )
    elif table == 'box':
        new_boxid = query_uid_by_type(db, table)
        new_name = obj.boxname
        if is_exist_name_by_table_parent_id(table, parent_id, obj.boxname, db):
            new_name = _copy_name(obj.boxname)
        new_id = add_freeze_box(
            new_name,
            new_boxid,
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
    # try:
    if dtype == 'folder':
        uparent = room.objects.filter(id=new_parent_id).first()
        if not uparent:
            return {'success': False, 'msg': u'新父节点不存在', 'code': 302}
        old_room = _find_by_id('room', uid, db)
        new_room_id = _copy_unit(old_room, 'room', str(room.parent_id), db)
        # 复制room下冰箱
        stores = query_storage_device_by_room_id(str(room.id), db)
        for store in stores:
            new_store_id = _copy_unit(store, 'storage', new_room_id, db)
            # 复制设备下冻存架
            shelfs = query_freeze_shelf_by_store_id(str(store.id), db)
            for shelf in shelfs:
                new_shelf_id = _copy_unit(shelf, 'shelf', new_store_id, db)
                # 复制冻存架下面冻存盒
                boxs = query_boxs_by_shelf_id(str(shelf.id), db)
                for box in boxs:
                    new_box_id = _copy_unit(box, 'box', new_shelf_id, db)
    elif dtype == 'storage':
        uroom = _find_by_id('room', new_parent_id, db)
        if not uroom:
            return {'success': False, 'msg': u'空间不存在', 'code': 302}
        store = _find_by_id('storage_device', uid, db)
        new_store_id = _copy_unit(store, 'storage', new_parent_id, db)
        # 复制设备下冻存架
        shelfs = query_freeze_shelf_by_store_id(str(store.id), db)
        for shelf in shelfs:
            new_shelf_id = _copy_unit(shelf, 'shelf', new_store_id, db)
            # 复制冻存架下面冻存盒
            boxs = query_boxs_by_shelf_id(str(shelf.id), db)
            for box in boxs:
                new_box_id = _copy_unit(box, 'box', new_shelf_id, db)
    elif dtype == 'freeze_shelf':
        ustorage = _find_by_id('storage_device', new_parent_id, db)
        if not ustorage:
            return {'success': False, 'msg': u'设备不存在', 'code': 302}
        shelf = _find_by_id('freeze_shelf', uid, db)
        new_shelf_id = _copy_unit(
            shelf, 'shelf', new_parent_id, db, new_postion)
        boxs = query_boxs_by_shelf_id(uid, db)
        for box in boxs:
            new_box_id = _copy_unit(box, 'box', new_shelf_id, db)
    elif dtype == 'freeze_box':
        shelf = _find_by_id('freeze_shelf', new_parent_id, db)
        if not shelf:
            return {'success': False, 'msg': u'冻存架不存在', 'code': 302}
        box = _find_by_id('freeze_box', uid, db)
        new_box = _copy_unit(box, 'box', new_parent_id, db, new_postion)
    return {'success': True, 'msg': u'', 'code': 200}
    # except:
    #   return {'success': False, 'msg': u'复制失败,数据库错误', 'code': 301}


def add_room(name, rank, parent_id, db):
    data = dict(
        name=name,
        rank=int(rank),  # 层级
        parent_id=parent_id,
        roomtype='folder'
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


def add_new_storage(storagename, terminalname, storageid, utype, dtype, rank, room_id, storageline=10, storagecolumn=10, db=None):
    data = dict(
        storagename=storagename,
        terminalname=terminalname,
        storageid=storageid,  # 设备自定义id
        storagetype=utype,
        detailtype=dtype,
        storageline=storageline,
        storagecolumn=storagecolumn,
        rank=int(rank),
        room_id=room_id
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


def add_freeze_shelf(shelfname, utype, dtype, shelfid, shelforder, rank, storage_id, hands_direction, shelfline=10, shelfcolumn=10, db=None, shelf_style='AAA'):
    data = dict(
        shelfname=shelfname,
        shelftype=utype,
        detailtype=dtype,
        shelfid=shelfid,
        shelforder=str(shelforder),
        shelfline=shelfline,
        shelfcolumn=shelfcolumn,
        rank=int(rank),
        storageid=storage_id,
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


def add_freeze_box(boxname, boxid, utype, dtype, boxorder, rank, shelf_id, box_note, boxline=10, boxcolumn=10, db=None):
    data = dict(
        boxname=boxname,
        boxid=boxid,         # 冻存盒自定义id
        boxorder=str(boxorder),   # 根据冻存架的类别确定1,11,A1
        boxtype=utype,
        detailtype=dtype,
        boxline=boxline,
        boxcolumn=boxcolumn,
        rank=int(rank),
        shelfid=shelf_id,
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


def add_sample(sample_id, box_id, sample_order, db, phone, username, img_url, sample_name=''):
    try:
        data = dict(
            sample_id=sample_id,
            box_id=box_id,
            sample_order=sample_order,
            sample_name=sample_name,
            img_url=img_url
        )
        insert_id = ""
        insert_id = _insert_one('sample', data, db)
        log = _insert_log(db, 'sample', 'add', str(insert_id))
        # TODO在此更新原库数据条目
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        mg[db]['level3mp'].update_one(
            {'_id': ObjectId(sample_id)},
            {
                '$set': {"if_bound": 1, "box_id": box_id, "orderid": sample_order, "img_url": img_url, 'sample_type': sample_name}
            }
        )
        box_id, shelf_id, storage_id = _query_step_ids_by_sample_id(
            sample_id, db)
        sample_log = _insert_sample_log(
            db=db,
            sample_id=sample_id,
            sample_define_id=sample.样本ID,
            old_box_id='',
            old_order='',
            old_shelf_id='',
            old_storage_id='',
            new_box_id=box_id,
            new_order=sample_order,
            new_shelf_id=shelf_id,
            new_storage_id=storage_id,
            op_user_phone=phone,
            op_user_name=username,
            op_type="入库"
        )
        _sample_out_true_log(sample_id, sample.样本ID,
                             sample_order, '', box_id, username, "入库", db)
        if not log:
            raise Exception('日志插入异常')
    except Exception as e:
        # 此处输入系统log
        print(e)
        return None
    return str(insert_id)


def query_item_by_code_by_id(utable, parent_id, code_name, db):
    try:
        code_name = int(code_name)
    except:
        code_name = str(code_name)
    if utable == 'storage':
        rst = _query('freeze_shelf', {
                     'storageid': parent_id, 'shelforder': code_name}, db)
        return rst[0] if rst else None
    elif utable == 'shelf':
        rst = _query('freeze_box', {
                     'shelfid': parent_id, 'boxorder': code_name}, db)
        return rst[0] if rst else None
    elif utable == 'box':
        rst = _query('sample', {'box_id': parent_id,
                                'sample_order': code_name}, db)
        return rst[0] if rst else None


def query_sample_by_box_id(box_id, db):
    rst = _find_all('level3mp', {'box_id': str(box_id)}, db)
    new_rst = []
    for i in rst:
        foo = {}
        foo['box_id'] = i.box_id
        foo['name'] = i.orderid
        foo['dname'] = ''
        foo['uname'] = _query_username_by_sample_id(i.parentid, db)
        foo['sample_name'] = i.sample_type
        foo['yangbenID'] = i.样本ID
        foo['id'] = i.id
        foo['img_url'] = _query_sample_image_by_name(i.样本种类, db)
        new_rst.append(foo)
    return new_rst


def _query_position_by_box(box_id, sample_order, db):
    # box_name
    box = query_freeze_box_by_id(box_id, db)
    box_name = box.boxname
    # freeze_name
    shelf = query_shelf_by_id(box.shelfid, db)
    shelf_name = shelf.shelfname
    # 设备name
    storage = query_storage_by_id(shelf.storageid, db)
    storage_name = storage.storagename
    return "//".join([storage_name, shelf_name, box_name, sample_order])


def query_sample_position(db):
    foo_rst = _find_all('level3mp', {"orderid": {"exists": True}}, db)
    rst = []
    for item in foo_rst:
        foo = {}
        foo['id'] = item.id
        foo['order'] = _query_position_by_box(item.box_id, item.order_id)
        rst.append(foo)
    return rst


def check_box_id_by_sample(sample_id, db):
    # 根据level3mp表检查box_id是否存在
    obj = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
    if obj and obj.box_id:
        return {'exist': True, 'box_id': obj.box_id}
    return {'exist': False}


def add_to_sample_check(sample_id, box_id, db):
    ''' 添加出库集合 '''
    #is_exist = _find_by_id('sample_check', sample_id, db)
    is_exist = mg[db]['sample_check'].find_one(
        {'sample_id': str(sample_id), 'is_deleted': {'$not': {'$eq': True}}})
    if is_exist:
        return True
    data = dict(
        sample_id=sample_id,
        box_id=box_id,
        check_rst=False,
        dt_create=now_ts()
    )
    try:
        _insert_one('sample_check', data, db)
    except:
        return False
    return True


def delete_from_sample_check(sample_ids, db):
    for sample_id in sample_ids:
        mg[db]['sample_check'].delete_one({'sample_id': str(sample_id)})
    return True


def _query_username_by_sample_id(level2mp_id, db):
    obj_level2 = _find_one('level2mp', {'_id': level2mp_id}, db)
    if not obj_level2:
        return ""
    obj_level1 = _find_one("level1mp", {"_id": obj_level2.parentid}, db)
    if obj_level1 and hasattr(obj_level1, '姓名'):
        return obj_level1.姓名
    else:
        return ""


def query_sample_check(db):
    foo_rst = _find_all(
        'sample_check', {'is_deleted': {'$not': {'$eq': True}}}, db)
    rst = []
    ch_status = {0: "未分配位子", 1: "在库", 2: "预出库", 3: "出库"}
    for item in foo_rst:
        obj = _find_one('level3mp', {'_id': ObjectId(item.sample_id), 'is_deleted': {
                        '$not': {'$eq': True}}}, db)
        if not obj:
            # 已经出库的条目
            continue
        foo = {}
        foo['id'] = item.sample_id
        foo['order'] = _query_position_by_box(item.box_id, obj.orderid, db)
        foo['name'] = obj.样本种类
        foo['uname'] = _query_username_by_sample_id(obj.parentid, db)
        foo['sample_define_id'] = obj.样本ID
        foo['sample_branh_num'] = obj.样本分管号
        foo['status'] = ch_status.get(obj.if_bound, '')
        rst.append(foo)
    return rst


def add_sample_apply(sample_ids, apply_user, op_user, reason, db):
    ''' 添加出库申请 '''
    rst = query_sample_check(db)
    sample_ids = [i['id'] for i in rst]
    sample_status = {}
    for sample_id in sample_ids:
        obj = _find_one('level3mp', {'_id': ObjectId(sample_id), 'is_deleted': {
                        '$not': {'$eq': True}}}, db)
        sample_status[sample_id] = {
            'status': 2, 'order': _query_position_by_box(obj.box_id, obj.orderid, db)}
    data = dict(
        sample_ids=sample_status,
        sample_num=len(sample_ids),
        apply_user=apply_user,
        op_user=op_user,
        reason=reason,
        sample_status=2,     # 预出库
        dt_create=now_ts()
    )
    _insert_one('sample_out_apply', data, db)
    # 更新level3mp表if_bound
    for sample_id in sample_ids:
        mg[db]['level3mp'].update_one(
            {'_id': ObjectId(sample_id)},
            {
                '$set': {"if_bound": 2}
            }
        )
        # 移出出库集,更新is_deleted=True
        _update_one("sample_check",
                    {"sample_id": str(sample_id), "is_deleted": {
                        '$not': {'$eq': True}}},
                    {"is_deleted": True}, db)
        #mg[db]['sample_check'].remove({'sample_id': str(sample_id)})
    return True


def query_check_status_by_sample_id(sample_id, db):
    sample_check = _find_one('sample_check', {'sample_id': str(sample_id)}, db)
    return sample_check.check_rst


def _query_sample_detail_by_ids(sample_ids, db):
    rst = []
    ch_status = {0: "未分配位子", 1: "在库", 2: "预出库", 3: "出库"}
    exist_out_true_sample = False
    for sample_id in sample_ids:
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        if sample.if_bound == 3:
            exist_out_true_sample = True
            break
    if exist_out_true_sample:
        ch_status = {0: "未分配位子", 1: "在库", 2: "在库", 3: "出库"}

    # for sample_id,item_status in sample_ids.items():
    count = 0
    for sample_id in sample_ids:
        item_status = sample_ids[sample_id]['status']
        item_order = sample_ids[sample_id]['order']
        if item_status == 3:
            count += 1
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        #sample = _find_one('level3mp', {'_id': ObjectId(sample_id), 'is_deleted': {'$not': {'$eq': True}}}, db)
        # if not sample:
        #    continue
        foo = {}
        foo['id'] = sample.id
        #foo['order'] = _query_position_by_box(sample.box_id, sample.orderid, db) if sample.if_bound != 3 else ''
        #foo['order'] = _query_position_by_box(sample.box_id, sample.orderid, db) if sample.box_id != '' else ''
        foo['order'] = item_order
        foo['name'] = sample.样本种类
        foo['value'] = sample.id
        foo['status'] = ch_status.get(item_status, "")
        foo['uname'] = _query_username_by_sample_id(sample.parentid, db)
        foo['sample_define_id'] = sample.样本ID
        foo['sample_branh_num'] = sample.样本分管号
        foo['check_rst'] = query_check_status_by_sample_id(sample_id, db)
        # 以后添加其他的字段
        rst.append(foo)
    return rst, count


def _query_apply_sample_ids(sample_ids, db):
    rst = {}
    for sample_id in sample_ids:
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        #rst[sample.样本二维码] = sample_id
        rst[sample_id] = sample_id
    return rst


def query_sample_apply_out(db, is_already, is_admin, current_user):
    ''' 获取出库申请 '''
    foo_rst = _find_all('sample_out_apply', {}, db)
    rst = []
    ch_status = {0: "未分配位子", 1: "在库", 2: "申请中", 3: "已完成"}
    for item in foo_rst:
        foo = {}
        if not is_admin:
            if current_user != item.apply_user:
                continue
        if int(is_already):
            if item.sample_status != 3:
                continue
        else:
            if int(item.sample_status) != 2:
                continue
        foo['id'] = item.id
        foo['num'] = item.sample_num
        foo['op_user'] = item.op_user
        foo['apply_user'] = item.apply_user
        foo['reason'] = item.reason
        foo['status'] = ch_status.get(int(item.sample_status), "")
        foo['dt_create'] = item.dt_create
        foo['detail'], foo['out_count'] = _query_sample_detail_by_ids(
            item.sample_ids, db)
        rst.append(foo)
    return rst


def _query_all_sample_two_code(db):
    '''获取level3mp表所有二维码信息'''
    rst = _find_all('level3mp', {}, db)
    # return [i.样本二维码 for i in rst]
    return [i.id for i in rst]


def check_id_in_sample_apply(code, apply_id, db):
    sample_apply = _find_by_id('sample_out_apply', str(apply_id), db)
    code_ids = _query_apply_sample_ids(sample_apply.sample_ids, db)
    real_ids = [k for k, v in code_ids.items()]
    all_ids = _query_all_sample_two_code(db)
    if code in real_ids:
        # 更新检测结果
        _update_one("sample_check", {"sample_id": code_ids[code]}, {
                    "check_rst": True}, db)
        return {"success": True}
    else:
        if code not in _query_all_sample_two_code(db):
            return {"success": False, "msg": u"样本id:{code},在样本库中不存在!".format(code=code)}
        return {"success": False, "msg": u"样本id:{code},在出库集中不存在!".format(code=code)}


def _sample_out_true_log(sample_id, sample_define_id, detail_order, apply_id, box_id, op_user, op_type, db):
    if not apply_id:
        my_apply = None
    else:
        my_apply = _find_by_id('sample_out_apply', str(apply_id), db)
    sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
    data = dict(
        sample_id=sample_id,
        sample_define_id=sample_define_id,
        box_id=box_id,
        detail_order=detail_order,
        apply_user=my_apply.apply_user if my_apply else '',
        op_user=op_user,
        reason=my_apply.reason if my_apply else '',
        op_type=op_type,
        dt_create=now_ts()
    )
    _insert_one('sample_out_log', data, db)


def sample_out_true(sample_ids, apply_id, op_user, db):
    ''' 确认出库 '''
    # 在出库申请但未出库的条目，需要改回原始状态
    my_apply = _find_one("sample_out_apply", {"_id": ObjectId(apply_id)}, db)
    if my_apply.sample_status == 3:
        return False
    exist_ids = my_apply.sample_ids.keys()
    return_ids = [str(item)
                  for item in exist_ids if str(item) not in sample_ids]
    for sample_id in return_ids:
        mg[db]['level3mp'].update_one(
            {'_id': ObjectId(sample_id)},
            {
                '$set': {"if_bound": 1, "is_deleted": False}
            }
        )
    up_dict = my_apply.sample_ids
    # TODO 同一个冻存盒下其他样本添加冻融次数条目记录
    sample = _find_one('level3mp', {'_id': ObjectId(sample_ids[0])}, db)
    sample_list = _find_all('level3mp', {'box_id': str(
        sample.box_id), "is_deleted": {'$not': {'$eq': True}}}, db)
    sample_list_cut = list(set(sample_list).difference(set(sample_ids)))
    _sample_connect_out_log(
        apply_id=apply_id,
        box_id=sample.box_id,
        sample_objs=sample_list_cut,
        op_user=op_user,
        reason="",
        op_type="出库",
        db=db
    )
    for sample_id in sample_ids:
        # 更新level3mp表if_bound
        obj = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        box_id = obj.box_id
        if obj.if_bound == 3:
            continue
        # 插入log
        _, shelf_id, storage_id = _query_step_ids_by_sample_id(sample_id, db)
        sample_log = _insert_sample_log(
            db=db,
            sample_id=sample_id,
            sample_define_id=obj.样本ID,
            old_box_id=box_id,
            old_order=obj.orderid,
            old_shelf_id=shelf_id,
            old_storage_id=storage_id,
            new_box_id='',
            new_order='',
            new_shelf_id='',
            new_storage_id='',
            op_user_phone='',
            op_user_name=op_user,
            op_type="出库"
        )
        detail_order = obj.orderid
        mg[db]['level3mp'].update_one(
            {'_id': ObjectId(sample_id)},
            {
                '$set': {"if_bound": 3, "is_deleted": True, "orderid": "", "box_id": ""}
            }
        )
        # 更新sample_ids里状态:
        up_dict[sample_id]['status'] = 3
        up_dict[sample_id]['order'] = ''
        _sample_out_true_log(sample_id, obj.样本ID, detail_order,
                             apply_id, box_id, op_user, '出库', db)

    _update_one('sample_out_apply', {"_id": ObjectId(apply_id)}, {
        "sample_status": 3, "op_user": op_user, "sample_ids": up_dict}, db)
    return True


def query_have_out_sample_ids(db):
    all_apply = _find_all('sample_out_apply', {}, db)
    samples = []
    for item in all_apply:
        samples += item.sample_ids
    return set(samples)


def _sample_connect_out_log(apply_id, box_id, sample_objs, op_user, reason, op_type, db):
    for item in sample_objs:
        detail_order = item.orderid
        data = dict(
            # out_sample_id=out_sample_id,
            # out_sample_detail_id=out_sample_detail_id,
            # out_sample_detail_order=out_sample_detail_order,
            apply_id=apply_id,
            sample_id=item._id,
            sample_detail_id=item.样本ID,
            detail_order=detail_order,
            box_id=box_id,
            op_user=op_user,
            reason="",
            op_type="出库",
            dt_create=now_ts()
        )
        _insert_one('sample_connect_out_log', data, db)
    return True


def _query_step_ids_by_sample_id(sample_id, db):
    sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
    box_id = sample.box_id
    box = query_freeze_box_by_id(box_id, db)
    shelf_id = box.shelfid
    shelf = query_shelf_by_id(shelf_id, db)
    storage = query_storage_by_id(shelf.storageid, db)
    storage_id = storage._id
    return box_id, shelf_id, storage_id


def add_sample_log_cut_shelf(shelf_id, new_storage_id, op_user, op_phone, db):
    sample_ids = _query_sample_ids_by_shelf_id(str(shelf_id), db)
    for sample_id in sample_ids:
        box_id, shelf_id, storage_id = _query_step_ids_by_sample_id(
            sample_id, db)
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        sample_log = _insert_sample_log(
            db=db,
            sample_id=sample_id,
            sample_define_id=sample.样本ID,
            old_box_id=box_id,
            old_order=sample.orderid,
            old_shelf_id=shelf_id,
            old_storage_id=storage_id,
            new_box_id=box_id,
            new_order=sample.orderid,
            new_shelf_id=shelf_id,
            new_storage_id=new_storage_id,
            op_user_phone=op_phone,
            op_user_name=op_user,
            op_type="剪切"
        )
    return


def add_sample_log_cut_box(box_id, new_shelf_id, op_user, op_phone, db):
    sample_ids = _query_sample_ids_by_box_id(str(box_id), db)
    for sample_id in sample_ids:
        box_id, shelf_id, storage_id = _query_step_ids_by_sample_id(
            sample_id, db)
        sample = _find_one('level3mp', {'_id': ObjectId(sample_id)}, db)
        sample_log = _insert_sample_log(
            db=db,
            sample_id=sample_id,
            sample_define_id=sample.样本ID,
            old_box_id=box_id,
            old_order=sample.orderid,
            old_shelf_id=shelf_id,
            old_storage_id=storage_id,
            new_box_id=box_id,
            new_order=sample.orderid,
            new_shelf_id=new_shelf_id,
            new_storage_id=storage_id,
            op_user_phone=op_phone,
            op_user_name=op_user,
            op_type="剪切"
        )
    return


def _query_sample_ids_by_shelf_id(shelf_id, db):
    boxs = query_boxs_by_shelf_id(shelf_id, db)
    rst = []
    for box in boxs:
        samples = _query_sample_ids_by_box_id(box._id, db)
        rst += samples
    return rst


def _query_sample_ids_by_box_id(box_id, db):
    rst = _find_all('level3mp', {'box_id': str(
        box_id), 'is_deleted': {'$not': {'$eq': True}}}, db)
    return [i._id for i in rst]


def format_name_list_by_data(field_info, level):
    rst = []
    if level == 1:
        for item in field_info:
            rst.append(item['value'])
    elif level == 2:
        for item in field_info:
            name_1 = item['value']
            for obj2 in item.get('list', []):
                name_2 = obj2['value']
                rst.append(name_1 + '-' + name_2)
    elif level == 3:
        for item in field_info:
            name_1 = item['value']
            for obj2 in item.get('list', []):
                name_2 = obj2['value']
                for obj3 in obj2.get('list', []):
                    name_3 = obj3['value']
                    rst.append(name_1 + '-' + name_2 + '-' + name_3)
    return rst


def query_sample_image_db(db):
    #field_info = _find_one("custorm_fields", {"sfybzl": {'$not': {'$eq': False}}}, db)
    #field_info = _find_one("custom_fields", {"sfybzl": {'$eq': True}}, db)
    field_info = _find_one("custom_fields", {"field_names": "样本种类"}, db)
    field_name_list = format_name_list_by_data(json.loads(
        field_info.drop_down_name), int(field_info.drop_down_level))
    #field_name_list = ["血清", "血浆", "肿瘤", "尿液"]
    """ field_info = _find_one("custom_fields", {"field_names": "样本种类"}, db)
    field_value = field_info.drop_down_name
    field_value = field_value.split(',')
    field_name_list = []
    for x in field_value:
        if x != "请选择":
            field_name_list.append(x) """
    rst = []
    for name in field_name_list:
        foo = {}
        foo['name'] = name
        foo["img"] = _query_sample_image_by_name(name, db)
        rst.append(foo)
    return rst


def update_image_by_name_db(name, img_base64, db):
    obj_img = _find_one("sample_img", {"name": name}, db)
    if not obj_img:
        _insert_one("sample_img", {"name": name, "img": img_base64}, db)
    else:
        _update_one("sample_img", {"name": name}, {"img": img_base64}, db)
    return True


def _query_sample_image_by_name(name, db):
    obj_img = _find_one("sample_img", {"name": name}, db)
    if obj_img:
        return obj_img.img
    else:
        return ""


def query_uid_by_type(db, utype):
    if utype == 'storage':
        obj = mg[db]['storage_device'].find(
            {}, limit=1, sort=[("storageid", pymongo.DESCENDING)])
        obj = [i for i in obj]
        if not obj:
            uid = '900001'
        else:
            uid = str(int(obj[0]['storageid']) + 1)
    elif utype == 'shelf':
        obj = mg[db]['freeze_shelf'].find(
            {}, limit=1, sort=[("shelfid", pymongo.DESCENDING)])
        obj = [i for i in obj]
        if not obj:
            uid = '800001'
        else:
            uid = str(int(obj[0]['shelfid']) + 1)
    elif utype == 'box':
        obj = mg[db]['freeze_box'].find(
            {}, limit=1, sort=[("boxid", pymongo.DESCENDING)])
        obj = [i for i in obj]
        if not obj:
            uid = '700001'
        else:
            uid = str(int(obj[0]['boxid']) + 1)
    return uid
