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
    length = column
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
        

def format_shelf_list(shelf_style, code_method, line, column, shelf_id):
    rst = []
    code_list = _shelf_code_method(line, column, shelf_style[0],shelf_style[1],shelf_style[2], code_method)
    for i in code_list:
        foo_list = []
        for j in i:
            foo = {}
            foo['percent'] = 0
            foo['name'] = j
            foo['dname'] = ''
            exist_child = query_item_by_code_by_id('shelf', str(shelf_id), j)
            if exist_child:
                foo['id'] = str(exist_child['id'])
                foo['percent'] = 1
                foo['dname'] = exist_child['boxname']
            foo_list.append(foo)
        rst.append(foo_list)
    '''
    else:
        for i in range(int(line)):
            foo_list = []
            for j in range(int(column)):
                foo = {}
                code_name = query_code_name_by_type(i*int(column)+j, code_method, line, column, 'freeze_shelf')
                foo['name'] = code_name
                foo['percent'] = 0
                foo['dname'] = ''
                #添加具体信息
                exist_child = query_item_by_code_by_id('shelf', str(shelf_id), str(code_name))
                if exist_child:
                    foo['id'] = str(exist_child['id'])
                    foo['percent'] = 1
                    foo['dname'] = exist_child['boxname']
                foo_list.append(foo)
            rst.append(foo_list)
    '''
    return rst

def format_box_list(code_method, line, column, box_id):
    code_list = [i for i in range(int(line)*int(column))]
    rst = []
    for i in range(int(line)*int(column)):
        foo = {}
        foo['percent'] = 0
        code_name = str(i)
        foo['name'] = code_name
        foo['dname'] = ''
        #exist_child = query_item_by_code_by_id('shelf', str(shelf_id), str(code_name))
        #if exist_child:
        #    foo['id'] = str(exist_child['id'])
        rst.append(foo)
    return rst

def format_storage_list(code_method, line, column, storage, parent_id, utable):
    rst = []    
    exist_item = 0
    if storage.startswith("yedanguan"):
        for i in range(column):
            foo = {}
            code_name = query_code_name_by_type(i, code_method, line, column, storage)
            foo['name'] = code_name
            exist_child = query_item_by_code_by_id(utable, str(parent_id), str(code_name))
            foo['percent'] = 0
            foo['dname'] = ''
            if exist_child:
                exist_item += 1
                foo['id'] = str(exist_child['id'])
                #foo['percent'] = _get_percent(exist_child, utable)
                foo['percent'] = 1
                if utable == 'storage':
                    foo['dname'] = exist_child['shelfname']
                elif utable == 'shelf':
                    foo['dname'] = exist_child['boxname']
            rst.append(foo)
        return rst
    for i in range(int(line)):
        foo_list = []
        for j in range(int(column)):
            foo = {}
            code_name = query_code_name_by_type(i*int(column)+j, code_method, line, column, storage)
            foo['name'] = code_name
            #添加具体信息
            exist_child = query_item_by_code_by_id(utable, str(parent_id), str(code_name))
            foo['percent'] = 0
            foo['dname'] = ''
            if exist_child:
                exist_item += 1
                foo['id'] = str(exist_child['id'])
                foo['percent'] = 1
                if utable == 'storage':
                    foo['dname'] = exist_child['shelfname']
                elif utable == 'shelf':
                    foo['dname'] = exist_child['boxname']
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


def _shelf_code_method(line, column, rule1,rule2,rule3, code_method):
    # rule1 -> 横纵转换
    # rule2 -> 左右
    # rule3 -> 上下
    en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I', '10': 'J', '11': 'K', '12': 'L', '13': 'M', '14': 'N'}
    line = int(line)
    column = int(column)
    rst = []
    if rule1 == 'A':
        for i in range(line):
            foo = []
            for j in range(1,column+1):
                unit = i*int(column)+j
                if code_method == '2':
                    unit = str(i+1) + str(unit)
                elif code_method == '3':
                    unit = en_ch.get(str(i+1)) + str(unit)
                foo.append(unit)
            if rule2 == 'B':
                foo.reverse()
            rst.append(foo)
    elif rule1 == 'B':
        for i in range(1,line+1):
            foo = []
            for j in range(column):
                foo_unit = j*int(line)+i
                if code_method == '1':
                    foo.append(foo_unit)
                elif code_method == '2':
                    ustr = str(i) + str(foo_unit)
                    foo.append(ustr)
                elif code_method == '3':
                    ustr = en_ch.get(str(i)) + str(foo_unit)
                    foo.append(ustr)
            if rule2 == 'B':
                foo.reverse()
            rst.append(foo)
    if rule3 == 'B':
        # 外层倒序
        rst.reverse()
    return rst



   
