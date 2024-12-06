# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-10-15 18:30:21
@LastEditTime: 2024-11-22 09:41:25
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class MemberEventModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', db_config_dict=None, sub_table=None, db_transaction=None, context=None):
        super(MemberEventModel, self).__init__(MemberEvent, sub_table)
        if not db_config_dict:
            db_config_dict = config.get_value(db_connect_key)
        self.db = MySQLHelper(db_config_dict)
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    # 方法扩展请继承此类

class MemberEvent:
    def __init__(self):
        super(MemberEvent, self).__init__()
        self.id = 0
        self.business_id = 0  # 商家标识
        self.one_id = ""  # one_id
        self.event_type = 0  # 事件类型(1-绑定 2-入会 3-退会 4-激活 5-注册 6-合并)
        self.event_reason = ""  # 事件原因
        self.event_desc = "" # 事件描述
        self.create_date = '1970-01-01 00:00:00.000' # 创建时间

    @classmethod
    def get_field_list(cls):
        return ['id', 'business_id', 'one_id', 'event_type', 'event_reason', 'event_desc', 'create_date']

    @classmethod
    def get_primary_key(cls):
        return "id"

    def __str__(self):
        return "member_event_tb"