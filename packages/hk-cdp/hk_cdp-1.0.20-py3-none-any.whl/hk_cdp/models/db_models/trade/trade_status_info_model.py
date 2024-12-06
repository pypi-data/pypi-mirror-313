# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-06 18:48:03
@LastEditTime: 2024-11-08 17:49:47
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class TradeStatusInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', db_config_dict=None, sub_table=None, db_transaction=None, context=None):
        super(TradeStatusInfoModel, self).__init__(TradeStatusInfo, sub_table)
        if not db_config_dict:
            db_config_dict = config.get_value(db_connect_key)
        self.db = MySQLHelper(db_config_dict)
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class TradeStatusInfo:
    def __init__(self):
        super(TradeStatusInfo, self).__init__()
        self.id = 0 # id
        self.user_id = 0  # 客户ID
        self.business_id = 0 # 商家标识
        self.store_id = 0 # 店铺标识
        self.main_pay_order_no = '' # 主订单号
        self.order_status = '' # 订单状态
        self.platform_id = 0  # # 平台标识
        self.end_date = 0  # # 完成时间
        self.is_sync = 0 # 是否同步
        self.sync_date = '1970-01-01 00:00:00.000' # 同步时间

    @classmethod
    def get_field_list(self):
        return ['id','user_id', 'business_id', 'store_id', 'main_pay_order_no', 'order_status', 'platform_id', 'end_date', 'main_pay_order_no', 'is_sync', 'sync_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "trade_status_info_tb"
