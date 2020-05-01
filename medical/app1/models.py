import mongoengine
import datetime
from django.db import models
import pytz
from datetime import datetime

# Create your models here.
def now_ts(lite=False):
    if lite:
        return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
    return datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

class room(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    parent_id = mongoengine.StringField(max_length=32)    # 父级id,只能是房间
    rank = mongoengine.IntField()                   # 层级
    roomtype = mongoengine.StringField(max_length=16, default='folder')  # 默认'folder'文件夹

class storage_device(mongoengine.Document):
    # 存储设备(比如冰箱,液氮罐)
    storageid = mongoengine.StringField(max_length=64)     #设备自定义id
    storagename = mongoengine.StringField(max_length=32)
    terminalname = mongoengine.StringField(max_length=32)  # 终端名称
    storagetype = mongoengine.StringField(max_length=16)   #液氮罐 冰箱
    detailtype = mongoengine.StringField(max_length=16, default='0')    #液氮罐 冰箱 具体类型,没有就是0
    storageline = mongoengine.IntField()
    storagecolumn = mongoengine.IntField()
    room_id = mongoengine.StringField(max_length=32)       # 父级id,只能是房间
    rank = mongoengine.IntField()                    # 层级

class freeze_shelf(mongoengine.Document):
    # 冻存架(放在冰箱里)
    storageid = mongoengine.StringField(max_length=64)       # 设备id
    shelforder = mongoengine.StringField(max_length=16)      # 顺序号(用于存储冻存架的顺序)
    shelfname = mongoengine.StringField(max_length=32)
    hands_direction = mongoengine.StringField(max_length=16) # 拉手方向
    shelftype = mongoengine.StringField(max_length=32)       # 冻存架排列方式两种(正序,逆序)
    detailtype = mongoengine.StringField(max_length=16, default='0')    #冻存架类别(立式)
    shelfline = mongoengine.IntField()
    shelfecolumn = mongoengine.IntField()
    rank = mongoengine.IntField()                    # 层级

class freeze_box(mongoengine.Document):
    # 冻存盒(放在冻存架上)
    shelfid = mongoengine.StringField(max_length=64)       #冻存架id
    boxorder = mongoengine.StringField(max_length=16)                      #顺序号(用于存储冻存架的顺序)
    boxfname = mongoengine.StringField(max_length=32)
    boxid = mongoengine.StringField(max_length=32)         #冻存盒自定义id
    boxtype = mongoengine.StringField(max_length=32)       
    boxline = mongoengine.IntField()
    boxcolumn = mongoengine.IntField()
    boxnote = mongoengine.StringField(max_length=256, default="")
    rank = mongoengine.IntField()                    # 层级

class log_info(mongoengine.Document):
    operate_table = mongoengine.StringField(max_length=32) # 操作表
    operate_type = mongoengine.StringField(max_length=16)  # 操作类别add, delete, update
    operate_id = mongoengine.StringField(max_length=64)    # 操作对象的id
    operate_desc = mongoengine.StringField(max_length=256, default="")
    destination_id = mongoengine.StringField(max_length=64, default="")   # 目的id,update时候用
    dt_create = mongoengine.DateTimeField(now_ts())

# 暂时不用
class room_storage_relation():
    rank = mongoengine.IntField()                 # 层级
    uid = mongoengine.StringField(max_length=32)        # 房间或是设备的id
    utype = mongoengine.StringField(max_length=16)      # 房间(room)或是设备(storage)
    parent_id = mongoengine.StringField(max_length=32)  # 父级id,只能是房间


