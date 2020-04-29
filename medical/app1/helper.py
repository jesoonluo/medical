import pytz
from mongoengine import StringField,FloatField,IntField,ListField,ObjectIdField
from datetime import datetime

def now_ts(lite=False):
    if lite:
        return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
    return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

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
