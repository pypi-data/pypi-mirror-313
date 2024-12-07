# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2023-02-09 18:29:31
@LastEditTime: 2023-04-17 14:01:18
@LastEditors: HuangJianYi
:Description: 全局share配置
"""

import json
import threading
from seven_framework import config

_lock = threading.Condition()


def init_config(path):
    """
    :Description: 初始化配置文件
    :param path: 配置文件路径，可使用物理路径或url
    :return: global share_app_config
    :last_editors: HuangJianYi
    """
    if path.lower().find("http://") > -1:
        import requests
        json_str = requests.get(path)
    else:
        with open(path, "r+", encoding="utf-8") as f:
            json_str = f.read()
    global share_app_config
    share_app_config = json.loads(json_str)


def set_value(key, value):
    """
    :Description: 设置一个全局键值配置
    :param key:参数键名
    :param value:参数值
    :return: 无
    :last_editors: HuangJianYi
    """
    _lock.acquire()
    try:
        share_app_config[key] = value
    except:
        raise
    finally:
        _lock.release()


def get_value(key, default_value=None):
    """
    :Description: 获得一个全局变量,不存在则返回默认值
    :param key:参数键名
    :param default_value:获取不到返回的默认值
    :return: 参数值
    :last_editors: HuangJianYi
    """
    config_value = config.get_value(key)
    if config_value == None:
        try:
            _lock.acquire()
            config_value = share_app_config[key]
            if config_value == None:
                config_value = default_value
        except KeyError:
            config_value = default_value
        except NameError:
            config_value = default_value
        finally:
            _lock.release()
    return config_value