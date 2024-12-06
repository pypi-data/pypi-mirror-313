# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-06 09:39:45
@LastEditTime: 2024-11-26 17:42:25
@LastEditors: HuangJianYi
@Description: 
"""

# 此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class StoreInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(StoreInfoModel, self).__init__(StoreInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    # 方法扩展请继承此类

class StoreInfo:

    def __init__(self):
        super(StoreInfo, self).__init__()
        self.id = 0  # id
        self.guid = None  # guid
        self.business_id = 0  # 商家标识
        self.platform_id = 0  # 平台类型
        self.store_name = ""  # 店铺名称
        self.seller_nick = ""  # 店铺主账号
        self.seller_id = "" # 店铺主账号id
        self.store_icon = ""  # 店铺图标
        self.plat_store_id = ""  # 平台店铺标识
        self.store_status = 0  # 店铺状态
        self.plat_telephone_key = ""  # 平台手机号密钥
        self.prefix_status = 0  # 号段生成状态
        self.prefix_path = ""  # 号段存储路径
        self.overdue_date = '1970-01-01 00:00:00.000'  # 过期时间
        self.access_token = ""  # access_token
        self.description = ""  # 描述
        self.cdp_rawdata_sync_status = 0  # cdp_原始数据同步状态
        self.create_date = '1970-01-01 00:00:00.000'  # 创建时间
        self.modify_date = '1970-01-01 00:00:00.000'  # 修改时间

    @classmethod
    def get_field_list(cls):
        return [
            'id', 'guid', 'business_id', 'platform_id', 'store_name', 
            'seller_nick', 'seller_id', 'store_icon', 'plat_store_id', 'store_status', 
            'plat_telephone_key', 'prefix_status', 'prefix_path', 
            'overdue_date', 'access_token', 'description', 
            'cdp_rawdata_sync_status', 'create_date', 'modify_date'
        ]
        
    @classmethod
    def get_primary_key(cls):
        return "id"

    def __str__(self):
        return "store_info_tb"
