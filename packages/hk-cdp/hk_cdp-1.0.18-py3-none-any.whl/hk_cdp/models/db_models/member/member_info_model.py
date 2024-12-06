# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-10-15 18:30:21
@LastEditTime: 2024-11-15 11:45:11
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class MemberInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', db_config_dict=None, sub_table=None, db_transaction=None, context=None):
        super(MemberInfoModel, self).__init__(MemberInfo, sub_table)
        if not db_config_dict:
            db_config_dict = config.get_value(db_connect_key)
        self.db = MySQLHelper(db_config_dict)
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    # 方法扩展请继承此类

class MemberInfo:
    def __init__(self):
        super(MemberInfo, self).__init__()
        self.id = 0  # id
        self.one_id = ""  # one_id
        self.business_id = 0  # 商家标识
        self.scheme_id = 0  # 会员体系标识
        self.include_plattypes = {}  # 归属平台
        self.include_stores = {}  # 归属店铺
        self.level_id = 0  # 会员等级标识
        self.level_valid_date = '1970-01-01 00:00:00.000'  # 会员等级有效期
        self.member_telephone = ""  # 会员手机号
        self.real_name = ""  # 姓名
        self.birthday = '1970-01-01 00:00:00.000'  # 生日
        self.sex = 0  # 性别(0-未知 1-男 2-女)
        self.first_ouid = ""  # 首绑ouid
        self.first_store_integral = 0  # 首绑店铺积分
        self.first_plat_store_id = ""  # 首绑平台店铺标识
        self.first_join_date = '1970-01-01 00:00:00.000'  # 首次入会时间
        self.first_join_store_id = 0  # 首次入会店铺
        self.last_join_date = '1970-01-01 00:00:00.000'  # 最近入会时间
        self.last_join_store_id = 0  # 最近入会店铺
        self.extend_info = {}  # 扩展信息json
        self.member_status = 1  # 状态(0-合并删除 1-会员 2-非会员)
        self.is_one_merge = 0 # 是否oneid合并中（1-是 0-否）
        self.create_date = '1970-01-01 00:00:00.000'  # 创建时间
        self.modify_date = '1970-01-01 00:00:00.000'  # 修改时间

    @classmethod
    def get_field_list(cls):
        return [
            'id', 'one_id', 'business_id', 'scheme_id', 'include_plattypes', 'include_stores', 'level_id', 
            'level_valid_date', 'member_telephone', 'real_name', 'birthday', 'sex', 'first_ouid', 
            'first_store_integral', 'first_plat_store_id', 'first_join_date', 'first_join_store_id', 
            'last_join_date', 'last_join_store_id', 'extend_info', 'member_status', 'is_one_merge', 'create_date', 'modify_date'
        ]

    @classmethod
    def get_primary_key(cls):
        return "id"

    def __str__(self):
        return "member_info_tb"
