# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-10-15 18:30:21
@LastEditTime: 2024-11-14 15:22:28
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class MemberAssetValidModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', db_config_dict=None, sub_table=None, db_transaction=None, context=None):
        super(MemberAssetValidModel, self).__init__(MemberAssetValid, sub_table)
        if not db_config_dict:
            db_config_dict = config.get_value(db_connect_key)
        self.db = MySQLHelper(db_config_dict)
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    # 方法扩展请继承此类

class MemberAssetValid:
    def __init__(self):
        super(MemberAssetValid, self).__init__()
        self.id = 0
        self.change_no = ""  # 变更流水号(流水表的流水号)
        self.valid_end_day = 19700101  # 有效期结束时间
        self.remark = ""  # 备注
        self.create_date = '1970-01-01 00:00:00.000'  # 创建时间
        self.is_process = 0  # 是否处理(0-否 1-是)
        self.process_date = '1970-01-01 00:00:00.000'  # 处理时间

    @classmethod
    def get_field_list(cls):
        return [
            'id', 'change_no', 'valid_end_day', 'remark', 'create_date', 'is_process', 'process_date'
        ]

    @classmethod
    def get_primary_key(cls):
        return "id"

    def __str__(self):
        return "member_asset_valid_tb"