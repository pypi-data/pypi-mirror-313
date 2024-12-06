# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2024-01-18 18:19:58
@LastEditTime: 2024-11-27 19:45:15
@LastEditors: HuangJianYi
:Description: 框架DB操作类
"""
from seven_framework.base_model import *
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *

class FrameDbModel(BaseModel):

    def __init__(self, model_class, sub_table):
        """
        :Description: 框架DB操作类
        :param model_class: 实体对象类
        :param sub_table: 分表标识
        :last_editors: HuangJianYi
        """
        super(FrameDbModel,self).__init__(model_class, sub_table)

    def add_list_batch(self, data_list, batch_num=100):
        """
        :description: 分批添加数据
        :param data_list：数据列表
        :param batch_num：分批数量
        :return 成功添加的数量
        :last_editors: HuangJianYi
        """
        page_index = 0
        total = 0
        while True:
            add_list = data_list[page_index * batch_num:(page_index + 1) * batch_num]
            if not add_list:
                return total
            result = self.add_list(add_list)
            if result == True:
                total += len(add_list)
            page_index += 1

    def set_sub_table(self, object_id=''):
        """
        :description: 设置分表
        :param object_id:object_id
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        sub_table_config = share_config.get_value("sub_table_config",{})
        table_config = sub_table_config.get(table_name, None)
        if table_config and object_id:
            sub_table = SevenHelper.get_sub_table(object_id, table_config.get("sub_count", 10))
            if sub_table:
                # 数据库表名
                self.table_name = table_name.replace("_tb", f"_{sub_table}_tb")
        return self
    
    def set_view(self, view_name=''):
        """
        :description: 设置视图
        :param view_name:视图名
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        if not view_name:
            self.table_name = table_name.replace("_tb", "_view")
        else:
            self.table_name = view_name
        return self
    
    def relation_and_merge_dict_list(self, primary_dict_list, relation_db_model, relation_key_field, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表关联ID数组从关联表获取字典列表合并。
        :param primary_dict_list: 主表字典列表
        :param relation_db_model: 关联表关联model
        :param relation_key_field:  关联表关联字段
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if len(primary_dict_list) <= 0:
            return primary_dict_list
        # 检查relation_key_field是否已经在field中
        if field != "*" and relation_key_field not in field.split(","):
            field = f"{relation_key_field},{field}"
        ext_table_ids = [i[primary_key_field] for i in primary_dict_list]
        where = SevenHelper.get_condition_by_int_list(relation_key_field, ext_table_ids)
        if is_cache == True:
            relation_dict_list = relation_db_model.get_cache_dict_list(where, field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict_list = relation_db_model.get_dict_list(where, field=field)
        dict_list = SevenHelper.merge_dict_list(primary_dict_list, primary_key_field, relation_dict_list, relation_key_field, exclude_merge_columns_names="id")
        return dict_list
    
    def relation_and_merge_dict(self, primary_dict, relation_db_model, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表字典合并关联表字典。
        :param primary_dict: 主表字典
        :param relation_db_model: 关联表关联model
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if not primary_dict:
            return primary_dict
        if is_cache == True:
            relation_dict = relation_db_model.get_cache_dict_by_id(primary_dict[primary_key_field], field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict = relation_db_model.get_dict_by_id(primary_dict[primary_key_field], field=field)
        if relation_dict and "id" in relation_dict:
            del relation_dict["id"]
        if relation_dict:
            primary_dict.update(relation_dict)
        return primary_dict
    
    def call_procedure(self, procedure_name, params=None):
        """
        :Description: 调用存储过程
        :param procedure_name: 存储过程名称
        :param params: 参数值(元组)
        :return: 存储过程的结果
        """
        self.db.connection()
        try:
            with self.db._conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.callproc(procedure_name, params)
                result = cursor.fetchall()
            self.db._conn.commit()
            return result
        except Exception as e:
            self.db._conn.rollback()
            print(traceback.print_exc())
            raise Exception("mysql execute error:" + str(e) + " procedure:" +
                            str(procedure_name) + " 参数:" + str(params))
        finally:
            self.db._conn.close()
