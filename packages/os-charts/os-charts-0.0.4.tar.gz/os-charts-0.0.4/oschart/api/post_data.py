#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 2:09 PM
# @Author  : zy
# @Site    :
# @File    : charts_data.py
# @Software: PyCharm
"""
文件功能:
帖子相关信息
"""
from typing import Union
import datetime
import json


from oschart.database.database import os_chart_db, EsDb, MysqlDb
from oschart.utils.constant import platform_str_list, PLATFORM_DICT
from oschart.utils.os_error import os_charts_exception, OsChartsParamsError


class OsPost:
    """
    对外提供帖子信息类
    单主页时间段查询 默认提供最新100条post
    帖子id查询 提供全量 上限10000

    """

    def __init__(self, **kwargs):
        # 数据源
        self.db_es: EsDb = os_chart_db.get_db_es
        self.db_mysql: MysqlDb = os_chart_db.get_db_mysql
        # 必传
        self.page_id: str = kwargs.get("page_id")
        self.platform: str = kwargs.get("platform")
        # 看情况必传
        self.post_id: Union[str, list] = kwargs.get("post_id")
        self.date_start: str = kwargs.get("date_start")
        self.date_end: str = kwargs.get("date_end")
        # 可选传
        self.timezone: int = kwargs.get("timezone", 0)
        self.platform_int: int = kwargs.get("platform_int")
        self.post_ids: list = kwargs.get("post_ids")
        self.table_name: str = kwargs.get("table_name")
        self.limit: int = kwargs.get("limit", 100)
        self.__params_init_and_check()

    @os_charts_exception
    def get_post_data(self) -> dict:
        """
        帖子数据
        """
        res_data = {"total_posts": None, "post_data": list()}
        query_body = self.__init_es_sql()
        page_info = self.__get_page_info()
        with self.db_es as es_db_:
            res = es_db_.search(index=self.table_name, body=query_body)
            hits = res.get("hits", {})
            res_data.update({"total_posts": hits.get("total", {}).get("value")})
            for data_ in hits.get("hits", []):
                _source = data_.get("_source")
                if not _source:
                    continue
                _source.update(page_info)
                res_data["post_data"].append(_source)
        return res_data

    def __get_page_info(self) -> dict:
        """
        主页信息
        """
        res_ = dict()
        page_field = ["page_id", "page_name", "page_username", "page_image", "page_link"]
        from_sql = f"SELECT " + ", ".join(page_field) + " FROM social_page_info_v3 "
        where_sql = f"WHERE network={self.platform_int} AND page_id='{self.page_id}' ;"
        page_sql = from_sql + where_sql
        print(f"page_sql--{page_sql}")
        with self.db_mysql as mysql_db_:
            mysql_db_.execute(page_sql)
            page_set = mysql_db_.fetchone()
            if not page_set:
                return res_
            for field_key in page_field:
                field_key_data = page_set.get(field_key)
                res_[field_key] = field_key_data
        return res_

    def __params_init_and_check(self) -> None:
        """
        检查过滤字段规则格式 & 初始化其余字段
        :return:
        """
        if not self.page_id:
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info="page_id 参数不能为空",
            )
        if not self.platform:
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info="platform 参数不能为空",
            )
        if self.platform not in platform_str_list():
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info=f"{self.platform} not in {platform_str_list()}",
            )
        if self.post_id and not isinstance(self.post_id, (str, list)):
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info=f"{self.post_id} type must str or list",
            )
        if not self.post_id and not self.date_start and not self.date_end:
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info="date_stat/date_end 与 post_id 参数不可同时为空",
            )
        if self.date_start and self.date_end:
            try:
                datetime.datetime.strptime(self.date_start, "%Y-%m-%d")
                datetime.datetime.strptime(self.date_end, "%Y-%m-%d")
            except ValueError:
                raise OsChartsParamsError(
                    error_code="os-charts-param",
                    error_info="date_stat/date_end 格式不正确，例子：2023-01-01",
                )
        # ini
        if self.post_id and isinstance(self.post_id, str):
            self.post_ids = [self.post_id]
        if self.post_id and isinstance(self.post_id, list):
            self.post_ids = self.post_id
        self.platform_int = PLATFORM_DICT.get(self.platform)
        self.table_name = self.__get_table_name()

    def __get_table_name(self) -> str:
        """
        es 表名
        """
        platform_str = self.platform
        if platform_str == "vkontakte":
            platform_str = "vk"
        return f"page_posts_{platform_str}"

    def __edit_time_zone(self) -> str:
        """
        时区转换
        """
        if not isinstance(self.timezone, str):
            timezone = (
                "+" + str(self.timezone)
                if self.timezone >= 0
                else str(int(self.timezone))
            )
        else:
            timezone = self.timezone
        return timezone

    def __init_es_sql(self) -> dict:
        """
        生成 es query
        :return:
        """
        # query init
        query = {
            "bool": {
                "must": [],
                "must_not": [],
                "filter": [
                    {"terms": {"timeline_visibility": [1]}},
                    {"term": {"page_id": self.page_id}},
                ],
            }
        }
        if self.date_start and self.date_end:
            query["bool"]["must"].append(
                {
                    "range": {
                        "post_created_time": {
                            "gte": f"{self.date_start} 00:00:00",
                            "lt": f"{self.date_end} 23:59:59",
                            "time_zone": self.__edit_time_zone(),
                        }
                    }
                }
            )
        if self.post_ids:
            query["bool"]["must"].append({"terms": {"post_id": self.post_ids}})

        query_body = {
            "track_total_hits": True,
            "query": query,
            "aggregations": {},
            "sort": {"post_created_time": {"order": "desc"}},
            "size": self.post_ids.__len__() if self.post_ids else self.limit,
            "from": 0,
        }
        print(f"\nquery_body--{json.dumps(query_body)}")
        return query_body
