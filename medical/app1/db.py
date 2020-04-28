from medical.models import room,storage_devica,freeze_shelf,freeze_box
from bson.objectid import ObjectId

def init_node_room():
    exist = room.objects.filter(parent_id=0)
    if exist:
        return str(exist._id)
    new_first_node = room.objects.create(
        name = '全部空间',
        line_order = 1,                  # 层级
        parent_id = 0                   # 根节点
    )
    try:
        new_first_node.save()
    except:
        return None
    return new_first_node


def add_new_room(name, line_order, parent_id):
    new_node = room.objects.create(
        name = name,
        line_order = line_order,
        parent_id = parent_id                  
    )
    try:
        new_node.save()
    except:
        return None
    return str(new_node._id)

def query_all_room():
    return room.objects.all()

def query_all_room_ids():
    return [str(i._id) for i in room.objects.all()]

def query_storage_devica_by_room_id(room_id):
    return storage_devica.objects.filter(room_id=room_id).all()

def add_new_storage(storagename,utype,line_order,room_id):
    new_stora = storage_devica(
        storagename = storagename,
        storagetype = utype,
        storageline = 10,
        storagecolumn = 10,
        line_order = line_order,
        room_id = room_id
    )
    try:
        new_stora.save()
    except:
        return None
    return str(new_stora._id)
