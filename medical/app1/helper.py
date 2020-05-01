from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from .db import query_item_by_code_by_id


def mongo_to_dict_helper(obj):
    return_data = []
    for field_name in obj._fields:
        #if field_name in ("id",):
        #    continue
        data = obj._data[field_name]
        if isinstance(obj._fields[field_name], ObjectIdField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, int(data)))
        else:
            # You can define your logic for returning elements
            pass
    return dict(return_data)

def query_code_name_by_type(idx, code_method, line, column, storage):
    # 立式冰箱
    code_name = ''
    en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I', '10': 'J', '11': 'K', '12': 'L', '13': 'M', '14': 'N'}
    length = line
    if storage == 'fridge1':
        length = min(line, column)
    elif storage == 'fridge2':
        length = max(line, column)
    elif storage.startswith("yedanguan"):
        return idx + 1
    if code_method == '1': #1,2,3...,11
        code_name = idx + 1
    elif code_method == '2':   #11,21,31
        # 立式冰箱
        num_shang = idx//length + 1
        num_yu = idx%length + 1
        if num_yu == 0:
            code_name = str(num_shang) + str(1)
        code_name = str(num_shang) + str(num_yu)
    elif code_method  == '3':   #11,21,31
        num_shang = idx//length + 1
        num_yu = idx%length + 1
        if num_yu == 0:
            code_name = en_ch.get(str(num_shang)) + str(1)
        code_name = en_ch.get(str(num_shang)) + str(num_yu)
    return code_name
        

def format_storage_list(code_method, line, column, storage, parent_id, utable):
    rst = []    
    exist_item = 0
    if storage.startswith("yedanguan"):
        for i in range(column):
            foo = {}
            code_name = query_code_name_by_type(i, code_method, line, column, storage)
            foo['name'] = code_name
            exist_child = query_item_by_code_by_id(utable, parent_id, code_name)
            foo['percent'] = 0
            if exist_child:
                exist_item += 1
                foo['id'] = exist_child['id']
                foo['percent'] = _get_percent(exist_child, utable)
            rst.append(foo)
        return rst
    for i in range(int(line)):
        foo_list = []
        for j in range(int(column)):
            foo = {}
            code_name = query_code_name_by_type(i*int(column)+j, code_method, line, column, storage)
            foo['name'] = code_name
            #添加具体信息
            exist_child = query_item_by_code_by_id(utable, parent_id, code_name)
            foo['percent'] = 0
            if exist_child:
                exist_item += 1
                foo['id'] = exist_child['id']
                foo['percent'] = _get_percent(exist_child, utable)
            foo_list.append(foo)
        rst.append(foo_list)
    return rst
        
def _get_percent(obj, utable):
    if utable == 'storage':
        all_items = obj.shelfline*obj.shelfcolumn
        exist_items = len(freeze_shelf.objects.filter(storageid=obj.id).all())
    elif utable == 'shelf':
        all_items = obj.boxline*obj.boxcolumn
        exist_items = len(freeze_box.objects.filter(shelfid=obj.id).all())
    return round(exist_items/all_items*100)





   
