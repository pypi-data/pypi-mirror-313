# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-06 18:48:03
@LastEditTime: 2024-11-06 18:51:48
@LastEditors: HuangJianYi
@Description: 
"""
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class TradeRefundModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', db_config_dict=None, sub_table=None, db_transaction=None, context=None):
        super(TradeRefundModel, self).__init__(TradeRefund, sub_table)
        if not db_config_dict:
            db_config_dict = config.get_value(db_connect_key)
        self.db = MySQLHelper(db_config_dict)
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类


class TradeRefund:
    def __init__(self):
        super(TradeRefund, self).__init__()
        self.id = 0 # id
        self.refund_id = 0  # 退款号
        self.platform_id = 0  # # 平台标识
        self.seller_nick = ""  # 卖家昵称
        self.main_pay_order_no = '' # 主订单号
        self.sub_pay_order_no = '' # 子订单号
        self.refund_price = 0 # 退款金额
        self.is_sync = 0 # 是否同步
        self.sync_date = '1970-01-01 00:00:00.000' # 同步时间

    @classmethod
    def get_field_list(self):
        return ['id','refund_id', 'platform_id', 'seller_nick', 'main_pay_order_no', 'sub_pay_order_no', 'refund_price', 'is_sync', 'sync_date']

    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "trade_refund_tb"
