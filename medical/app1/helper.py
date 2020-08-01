from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from .db import query_item_by_code_by_id, query_samples_by_box_id, query_boxs_by_shelf_id


def mongo_to_dict_helper(obj):
    return_data = []
    for field_name,data in obj.items():
        #if field_name in ("id",):
        #    continue
        #data = obj._data[field_name]
        if isinstance(obj._fields[field_name], ObjectIdField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, list(data)))
        else:
            # You can define your logic for returning elements
            pass
    return dict(return_data)

def query_code_name_by_type(idx, code_method, line, column, storage):
    # 立式冰箱
    code_name = ''
    en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O'}
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


def format_shelf_list(shelf_style, code_method, line, column, shelf_id, db):
    rst = []
    code_list = _shelf_code_method(line, column, shelf_style[0],shelf_style[1],shelf_style[2], code_method)
    for i in code_list:
        foo_list = []
        for j in i:
            foo = {}
            foo['percent'] = 0
            foo['name'] = j
            foo['dname'] = ''
            exist_child = query_item_by_code_by_id('shelf', str(shelf_id), str(j), db)
            if exist_child:
                foo['id'] = str(exist_child.id)
                #foo['percent'] = 1
                foo['percent'] = _get_percent(exist_child, 'shelf', db)
                foo['dname'] = exist_child.boxname
            foo_list.append(foo)
        rst.append(foo_list)
    return rst

def format_box_list(code_method, line, column, box_id, db):
    code_list = [i for i in range(int(line)*int(column))]
    rst = []
    en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O'}
    for i in range(int(line)*int(column)):
        foo = {}
        foo['percent'] = 0
        #code_name = str(i)
        num_shang = i//int(line) + 1
        num_yu = i%int(line) + 1
        if num_yu == 0:
            code_name = en_ch.get(str(num_shang)) + str(1)
        else:
            code_name = en_ch.get(str(num_shang)) + str(num_yu)
        foo['name'] = code_name
        exist_child = query_item_by_code_by_id('box', str(box_id), str(code_name), db)
        if exist_child:
            foo['id'] = exist_child.sample_id
            foo['dname'] = exist_child.sample_name
        rst.append(foo)
    return rst

def format_storage_list(code_method, line, column, storage, parent_id, utable, db):
    rst = []
    exist_item = 0
    if storage.startswith("yedanguan"):
        for i in range(int(column)):
            foo = {}
            code_name = query_code_name_by_type(i, code_method, int(line), int(column), storage)
            foo['name'] = code_name
            exist_child = query_item_by_code_by_id('storage', str(parent_id), int(code_name), db)
            foo['percent'] = 0
            foo['dname'] = ''
            if exist_child:
                exist_item += 1
                foo['id'] = str(exist_child.id)
                foo['percent'] = _get_percent(exist_child, 'storage', db)
                #foo['percent'] = 1
                if utable == 'storage':
                    foo['dname'] = exist_child.shelfname
                elif utable == 'shelf':
                    foo['dname'] = exist_child.boxname
            rst.append(foo)
        return rst
    for i in range(int(line)):
        foo_list = []
        for j in range(int(column)):
            foo = {}
            code_name = query_code_name_by_type(i*int(column)+j, code_method, int(line), int(column), storage)
            foo['name'] = code_name
            #添加具体信息
            exist_child = query_item_by_code_by_id('storage', str(parent_id), str(code_name), db)
            foo['percent'] = 0
            foo['dname'] = ''
            if exist_child:
                exist_item += 1
                foo['id'] = str(exist_child.id)
                #foo['percent'] = 1
                foo['percent'] = _get_percent(exist_child, 'storage', db)
                if utable == 'storage':
                    foo['dname'] = exist_child.shelfname
                elif utable == 'shelf':
                    foo['dname'] = exist_child.boxname
            if foo['percent']:
                print('*'*10, foo['percent'])
            foo_list.append(foo)
        rst.append(foo_list)
    return rst

def _get_percent(obj, utable, db):
    if utable == 'storage':
        all_items = int(obj.shelfline)*int(obj.shelfcolumn)
        exist_items = len(query_boxs_by_shelf_id(str(obj.id), db))
    elif utable == 'shelf':
        all_items = int(obj.boxline)*int(obj.boxcolumn)
        exist_items = len(query_samples_by_box_id(str(obj.id), db))
    return round(exist_items/all_items*100)


def _shelf_code_method(line, column, rule1,rule2,rule3, code_method):
    # rule1 -> 横纵转换
    # rule2 -> 左右
    # rule3 -> 上下
    en_ch = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'J', '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O'}
    line = int(line)
    column = int(column)
    rst = []
    if rule1 == 'A':
        for i in range(line):
            foo = []
            for j in range(1,column+1):
                unit = i*int(column)+j
                #unit = j
                if code_method == '2':
                    unit = str(i+1) + str(j)
                elif code_method == '3':
                    unit = en_ch.get(str(i+1)) + str(j)
                foo.append(unit)
            if rule2 == 'B':
                foo.reverse()
            rst.append(foo)
    elif rule1 == 'B':
        for i in range(column):
            foo = []
            for j in range(1,line+1):
                unit = i*int(column)+j
                if code_method == '2':
                    unit = str(i+1) + str(j)
                elif code_method == '3':
                    unit = en_ch.get(str(i+1)) + str(j)
                foo.append(unit)
            if rule2 == 'B':
                foo.reverse()
            rst.append(foo)
    if rule3 == 'B':
        # 外层倒序
        rst.reverse()
    return rst




