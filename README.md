# 查询接口： 
###  Url:  http://118.24.161.188:8889/query_node
    
# 查寻冻存架： 
###  Url:  http://118.24.161.188:8889/query_shelfs?uid=设备id

# 添加存储空间:
###  Url: http://118.24.161.188:8889/add_room
###  请求方式: POST
```json
Param：{
"name": "房间名字", 
"rank": "rank等级(整型)", 
"parent_id": "父节点id"
}
```

# 删除:
###  Url: http://118.24.161.188:8889/delete_unit
###  请求方式: POST
```json
Param：{
   "uid": "要删除的id,有内容的空间不能删除(后端判定)",
   "dtype": "folder->文件夹, storage->设备, freeze_shelf->冻存架, freeze_box->冻存盒",
}
```

# 迁移剪切:
###  Url: http://118.24.161.188:8889/update_unit
###  请求方式: POST
```json
Param：{
   "uid": "要迁移id",  
   "new_parent_id": "迁移地儿的id",
   "dtype": "folder->文件夹, storage->设备, freeze_shelf->冻存架, freeze_box->冻存盒",
   "new_postion": "新冻存架的位子(在dtype为freeze_shelf时指定)"
}
```

# 迁移复制:
###  Url: http://118.24.161.188:8889/copy_unit
###  请求方式: POST
```json
Param：{
   "uid": "要复制id",  
   "new_parent_id": "复制地儿的id",
   "dtype": "folder->文件夹, storage->设备, freeze_shelf->冻存架, freeze_box->冻存盒",
}
```

# 重命名设备:
###  Url: http://118.24.161.188:8889/rename_unit
###  请求方式: POST
```json
Param：{
   "uid": "要重命名id",  
   "new_name": "新名字",
   "dtype": "folder->文件夹, storage->设备, freeze_shelf->冻存架, freeze_box->冻存盒",
}
```

# 添加存储设备:
### Url: http://118.24.161.188:8889/add_storage_device
### 请求方式: POST
```json
Param：{
"name": "存储设备名字",
"terminal_name": "终端名称",
"storage_id": "设备自定义id",
"rank": "rank等级(整型)", 
"parent_id": "存储空间id",
"utype": "存储设备编码类别",
"dtype": "存储设备详情-立式冰箱,卧式冰箱,或是冻存架类别",
"storageline": "冰箱行数(整型)", 
"storagecolumn": "冻存架列数(整型)",
}
```

# 添加液氮罐:
### Url: http://118.24.161.188:8889/add_storage_N2
### 请求方式: POST
```json
Param：{
"name": "存储设备名字",
"storage_id": "设备自定义id",
"rank": "rank等级(整型)", 
"parent_id": "存储空间id",
"utype": "液氮罐编码类别(默认1)",
"dtype": "液氮罐类别",
"num": "冻存架数量"
}
```

# 添加冻存架:
### Url: http://118.24.161.188:8889/add_freeze_shelf
### 请求方式: POST
```json
Param：{
"name": "冻存架名字", 
"rank": "rank等级(整型)", 
"parent_id": "存储设备id",
"utype": "冻存架类别（‘1’->正序，’2’->逆序)",
"dtype": "冻存架类别",
"shelfline": "冻存架行数(整型)", 
"shelfcolumn": "冻存架列数(整型)",
"shelf_order": "设备位子,A1",
"hands_direction": "拉手方向",
"shelf_style": "冻存架编码风格(AAA-默认,BBB.., 只有utype为1时即纯数字有效,2,3时此风格无效)"
}
```

# 添加冻存盒:
### Url: http://118.24.161.188:8889/add_freeze_box
### 请求方式: POST
```json
{
    "name": "冻存盒名字", 
    "rank": "rank等级(整型)", 
    "parent_id": "冻存架id",
    "utype": "冻存盒类别(‘1’，’2’，’3’)",
    "boxline": "冻存盒行数(整型)", 
    "boxcolumn": "冻存盒列数(整形)",
    "box_order": "冻存盒位子",
    "box_id": "冻存盒自定义id",
    "box_note": "冻存盒描述",
}
```

# 添加样本:
### Url: http://118.24.161.188:8889/add_sample
### 请求方式: POST
```json
{
    "data_list": [{"box_id": "冻存盒id", "sample_id": "样本id", "name":"box返回的order", "sample_name": "样本名字,可以不用传"},{}], 
}
```

# 查询冻存盒下样本： 
###  Url:  http://118.24.161.188:8889/query_samples?uid=冻存盒id
