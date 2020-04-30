# medical-
# 查询接口： 
###  Url:  http://118.24.161.188:8889/query_node
    
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

# 添加冻存架:
### Url: http://118.24.161.188:8889/add_freeze_shelf
### 请求方式: POST
```json
Param：{
"name": "冻存架名字", 
"rank": "rank等级(整型)", 
"parent_id": "存储设备id",
"utype": "冻存架类别（‘1’，’2’，’3’)",
"shelfline": "冻存架行数(整型)", 
"shelfcolumn": "冻存架列数(整型)"
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
    "boxid": "冻存盒自定义id",
    "boxnote": "冻存盒描述",
}
```
