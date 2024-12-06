
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *
from seven_cloudapp_frame.models.cache_model import *

class BusinessInfoModel(CacheModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None, context=None):
        super(BusinessInfoModel, self).__init__(BusinessInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class BusinessInfo:

    def __init__(self):
        super(BusinessInfo, self).__init__()
        self.id = 0  # id
        self.guid = None  # guid
        self.business_name = ""  # 商家名称
        self.is_release = 0  # 是否发布(1-是 0-否)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.business_code = ""  # 商家代码
        self.cdp_db_config = None  # cdp商家连接串

    @classmethod
    def get_field_list(self):
        return ['id', 'guid', 'business_name', 'is_release', 'create_date', 'modify_date', 'business_code', 'cdp_db_config']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "business_info_tb"
    