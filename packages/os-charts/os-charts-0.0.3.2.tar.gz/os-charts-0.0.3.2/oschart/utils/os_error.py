#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 11:09 AM
# @Author  : zy
# @Site    : 
# @File    : error.py
# @Software: PyCharm
"""
文件功能: 异常处理
"""
import functools
import json


class OsChartsError(Exception):
    """
    os chats 相关错误
    """

    def __init__(self, error_code=None, error_info=""):
        # 初始化父类
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return json.dumps(
            {"error_code": self.error_code, "error_info": self.error_info}
        )


class OsChartsParamsError(Exception):
    """
    os chats 参数相关错误
    """

    def __init__(self, error_code=None, error_info=""):
        # 初始化父类
        super().__init__(self)
        self.error_code = error_code
        self.error_info = error_info

    def __str__(self):
        return json.dumps(
            {"error_code": self.error_code, "error_info": self.error_info}
        )


def os_charts_exception(func_):
    """
    捕获异常
    """

    @functools.wraps(func_)  # 保留原始函数的元数据
    def wrapper(*args, **kwargs):
        """
        pass
        """
        try:
            return func_(*args, **kwargs)
        except Exception as e:
            raise OsChartsError(
                error_code="os-charts",
                error_info=str(e),
            )
    return wrapper
