import mongoengine
from django.db import models

# Create your models here.

class room(mongoengine.Document):
    name = mongoengine.StringField(max_length=32)
    line_order = mongoengine.IntField()                   # 层级
    parent_id = mongoengine.StringField(max_length=32)    # 父级id,只能是房间

class storage_device(mongoengine.Document):
    # 存储设备(比如冰箱,液氮罐)
    storagename = mongoengine.StringField(max_length=32)
    storagetype = mongoengine.StringField(max_length=16)   #液氮罐 冰箱
    storageline = mongoengine.IntField()
    storagecolumn = mongoengine.IntField()
    line_order = mongoengine.IntField()                    # 层级
    room_id = mongoengine.StringField(max_length=32)       # 父级id,只能是房间

class freeze_shelf(mongoengine.Document):
    # 冻存架(放在冰箱里)
    storageid = mongoengine.StringField(max_length=64)     #设备id
    shelforder = mongoengine.IntField()                    # 顺序号(用于存储冻存架的顺序)
    shelfname = mongoengine.StringField(max_length=32)
    shelftype = mongoengine.StringField(max_length=32)
    shelfline = mongoengine.IntField()
    shelfecolumn = mongoengine.IntField()

class freeze_box(mongoengine.Document):
    # 冻存盒(放在冻存架上)
    shelfid = mongoengine.StringField(max_length=64)       #冻存架id
    boxorder = mongoengine.IntField()                      #顺序号(用于存储冻存架的顺序)
    boxfname = mongoengine.StringField(max_length=32)
    boxid = mongoengine.StringField(max_length=32)         #冻存盒自定义id
    boxtype = mongoengine.StringField(max_length=32)
    boxline = mongoengine.IntField()
    boxcolumn = mongoengine.IntField()
    boxnote = mongoengine.GenericEmbeddedDocumentField()

# 暂时不用
class room_storage_relation():
    line_order = mongoengine.IntField()                 # 层级
    uid = mongoengine.StringField(max_length=32)        # 房间或是设备的id
    utype = mongoengine.StringField(max_length=16)      # 房间(room)或是设备(storage)
    parent_id = mongoengine.StringField(max_length=32)  # 父级id,只能是房间
