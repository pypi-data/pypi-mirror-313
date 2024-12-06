#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/3/8 10:50 AM
# @Author  : zy
# @Site    :
# @File    : database.py
# @Software: PyCharm
"""
文件功能:
数据库相关
"""

from dbutils.pooled_db import PooledDB
from elasticsearch import Elasticsearch
from pymysql.cursors import DictCursor
import pymysql.cursors


class SingletonMeta(type):
    """
    元类
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MysqlDb(metaclass=SingletonMeta):
    """
    mysql 客户端，采用单例模式和连接池管理数据库连接
    """

    def __init__(self, **connection_kwargs):
        super(MysqlDb, self).__init__()
        # 配置连接池
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            mincached=2,  # 连接池允许的最小连接数
            maxcached=5,  # 连接池允许的最大连接数
            maxshared=3,
            maxconnections=6,
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            host=connection_kwargs.get("host", ""),
            port=connection_kwargs.get("port", ""),
            user=connection_kwargs.get("user", ""),
            password=connection_kwargs.get("password", ""),
            database=connection_kwargs.get("database", ""),
            charset=connection_kwargs.get("charset", "utf8mb4"),
            cursorclass=pymysql.cursors.DictCursor,
        )

    def __enter__(self):
        self.conn, self.cs = self.get_conn()
        return self.cs

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交事务和关闭游标，连接由连接池管理自动回收，无需手动关闭
        self.conn.commit()
        self.cs.close()

    def get_conn(self):
        """从连接池中获取连接"""
        conn = self.pool.connection()
        cs = conn.cursor()
        return conn, cs

    def close_pool(self):
        """关闭连接池，通常在程序结束时调用"""
        self.pool.close()


class EsDb(object):
    """
    es 客户端
    """

    def __init__(self, **connection_kwargs):
        super(EsDb, self).__init__()
        # 初始化
        self.client = Elasticsearch(
            hosts=[{"host": connection_kwargs.get("host", ""), "port": connection_kwargs.get("port", "")}],
            http_auth=(connection_kwargs.get("user", ""), connection_kwargs.get("password", "")),
            scheme="http",
            timeout=100,
            max_retries=3,
            retry_on_timeout=True,
        )

    def __enter__(self):
        # 返回游标进行执行操作
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class OsChartsDb(object):
    """
    数据库配置类
    """

    def __init__(self):
        self._db_mysql = None
        self._db_es = None

    def set_mysql_config(self, **kwargs):
        """
        pass
        """
        self._db_mysql = MysqlDb(**kwargs)

    def set_es_config(self, **kwargs):
        """
        pass
        """
        self._db_es = EsDb(**kwargs)

    @property
    def get_db_mysql(self):
        """
        mysql 对象
        """
        return self._db_mysql

    @property
    def get_db_es(self):
        """
        es 对象
        """
        return self._db_es


os_chart_db = OsChartsDb()

