#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 2:09 PM
# @Author  : zy
# @Site    :
# @File    : charts_data.py
# @Software: PyCharm
"""
文件功能:

"""
from typing import Dict, Union, List, Any
from dataclasses import dataclass, field
import datetime
import json


from oschart.database.database import MysqlDb, os_chart_db, EsDb
from oschart.utils.chart_utils import get_date_list, data_to_week_or_month
from oschart.utils.constant import PLATFORM_INT_DICT
from oschart.utils.os_error import OsChartsParamsError, os_charts_exception
from oschart.utils.field_info import (
    FIELD_SETTINGS,
    MIDDLE_MODEL,
    INSIGHT_MODEL,
    ES_MODEL,
    SOCIAL_PAGE_SUMMARY,
    SOCIAL_PAGE_SUMMARY_INSIGHT,
    SOCIAL_PAGE_INSIGHT,
    ES_MODEL_MAPPINGS,
)


# TODO: is_last_sum  使用
@dataclass()
class BaseChartField:
    """
    BaseChart 字段示意
    此类只做备注使用
    """

    # 必填项
    date_start: str = field(metadata={"description": "开始时间"})
    date_end: str = field(metadata={"description": "结束时间"})
    page_id: str = field(metadata={"description": "主页id"})
    filed_key: Union[str, list] = field(metadata={"description": "统计字段"})

    # 非必填
    table_name: str = field(default="", metadata={"description": "表名"})
    platform: str = field(default="", metadata={"description": "平台"})
    timezone: int = field(default=0, metadata={"description": "时区"})
    date_source: str = field(default="mysql", metadata={"description": "数据源"})
    date_type: str = field(default="day", metadata={"description": "日周月"})
    date_field: str = field(default="created_at", metadata={"description": "时间筛选字段"})
    is_last_sum: bool = field(default=False, metadata={"description": "总计是否取最后一天"})
    is_last_date: bool = field(default=False, metadata={"description": "汇总取最新一天数据"})
    filed_key_list: List[str] = field(
        default_factory=list, metadata={"description": "list格式的统计字段"}
    )
    filter_field: Dict[str, Any] = field(
        default_factory=dict, metadata={"description": "过滤字段"}
    )
    # es数据源 独有
    buckets_key: str = field(
        default="sum", metadata={"description": "取值规则 sum avg count"}
    )
    # key value 格式表使用
    insight_key_name: str = field(default="key", metadata={"description": "授权表key值字段名"})
    insight_name_name: str = field(
        default="name", metadata={"description": "授权表name值字段名"}
    )


class FiledSetting:
    """
    字段配置
    """

    def __init__(self, **kwargs):
        self.field_keys: list = kwargs.get("field_keys", [])

    def analyze_filed_key_to_source(self) -> dict:
        """
        数据字段 同数据源输出
        """
        data_res = {
            "pub_field": list(),
            "auth_field": list(),
            "insight_field": list(),
            "es_field": list(),
            "other_field": list(),
        }
        for filed_key in self.field_keys:
            if filed_key in SOCIAL_PAGE_SUMMARY.keys():
                data_res["pub_field"].append(filed_key)
            elif filed_key in SOCIAL_PAGE_SUMMARY_INSIGHT.keys():
                data_res["auth_field"].append(filed_key)
            elif filed_key in SOCIAL_PAGE_INSIGHT.keys():
                data_res["insight_field"].append(filed_key)
            elif filed_key in ES_MODEL_MAPPINGS.keys():
                data_res["es_field"].append(filed_key)
            else:
                data_res["other_field"].append(filed_key)
        return data_res

    @property
    def get_field_settings(self) -> dict:
        """
        字段规则信息-all
        """
        return FIELD_SETTINGS

    @property
    def get_page_settings_pub(self) -> dict:
        """
        主页字段规则信息-公开
        """
        return SOCIAL_PAGE_SUMMARY

    @property
    def get_page_settings_auth(self) -> dict:
        """
        主页字段规则信息-授权
        """
        return {
            **SOCIAL_PAGE_SUMMARY_INSIGHT,
            **SOCIAL_PAGE_INSIGHT,
        }

    @property
    def get_post_settings(self) -> dict:
        """
        帖子字段
        """
        return ES_MODEL_MAPPINGS


class BaseChart:
    """
    基础类
    """

    def __init__(self, **kwargs):
        self.db_mysql: MysqlDb = os_chart_db.get_db_mysql
        self.db_es: EsDb = os_chart_db.get_db_es

        self.date_start: str = kwargs.get("date_start")
        self.date_end: str = kwargs.get("date_end")
        self.page_id: str = kwargs.get("page_id")
        self.filed_key: Union[str, list] = kwargs.get("filed_key")
        self.table_name: str = kwargs.get("table_name")
        self.platform: str = kwargs.get("platform")

        self.timezone: int = kwargs.get("timezone", 0)
        self.date_source: str = kwargs.get("date_source", "mysql")
        self.date_type: str = kwargs.get("date_type", "day")
        self.date_field: str = kwargs.get("date_field", "created_at")
        self.is_last_sum: bool = kwargs.get("is_last_sum", False)
        self.is_last_date: bool = kwargs.get("is_last_date", False)
        self.filed_key_list: List[str] = list()
        self.filter_field: Dict[str, Any] = dict()
        self.buckets_key: str = kwargs.get("buckets_key", "sum")
        self.insight_key_name: str = kwargs.get("insight_key_name", "key")
        self.insight_name_name: str = kwargs.get("insight_name_name", "name")
        self.__post_init__()

    def __post_init__(self):
        """
        默认项处理
        """

        field_settings = FIELD_SETTINGS.get(self.__get_filed_key_str(), {})
        for key, value in self.__dict__.items():
            setattr(self, key, field_settings.get(key, getattr(self, key)))

        # platform
        if not self.platform:
            self.platform = self.__get_page_platform()

        # filter_field 补偿 page_id
        if "page_id" not in self.filter_field.keys():
            self.filter_field["page_id"] = self.page_id

        # es table_name 自生成
        if self.date_source == "es":
            self.table_name = self.__get_es_index()

        # init filed_key_list
        self.filed_key_list = (
            self.filed_key if isinstance(self.filed_key, list) else [self.filed_key]
        )

        # check params
        self.__check_params_data()

    def init_res(self) -> dict:
        """
        初始化返回结构
        :return:
        """
        res_data = {
            "field_to_date": dict(),
            "field_to_sum": dict(),
        }
        date_list = get_date_list(start_date=self.date_start, end_date=self.date_end)
        for date_str in date_list:
            res_data["field_to_date"][date_str] = {
                key: None for key in self.filed_key_list
            }
        for key in self.filed_key_list:
            res_data["field_to_sum"][key] = None

        return res_data

    def init_res_os(self) -> dict:
        """
        初始化返回结构 os
        :return:
        """
        res_data = {
            "field_to_date": {"list": dict(), "max_min_sum_avg": dict()},
            "field_to_sum_list": list(),
            "field_to_sum_dict": dict(),
        }
        date_list = get_date_list(start_date=self.date_start, end_date=self.date_end)
        total_field_key = self.filed_key_list + ["total"]
        for date_str in date_list:
            res_data["field_to_date"]["list"][date_str] = {
                key: None for key in total_field_key
            }
            res_data["field_to_date"]["list"][date_str]["date"] = date_str

        for k in ["sum", "max", "min", "avg"]:
            for k_ in total_field_key:
                res_data["field_to_date"]["max_min_sum_avg"][f"{k}_{k_}"] = None
                if k in ["max", "min"]:
                    res_data["field_to_date"]["max_min_sum_avg"][
                        f"{k}_{k_}_date"
                    ] = None

        for k in self.filed_key_list:
            res_data["field_to_sum_dict"][k] = None

        return res_data

    def edit_res_data_os(self, res_data: dict) -> None:
        """
        整理返回结构
        :param res_data:
        :return:
        """
        # 数据格式转换 os
        res_data["field_to_date"]["list"] = [
            value for _, value in res_data["field_to_date"]["list"].items()
        ]
        res_data["field_to_sum_list"] = [
            {"name": k, "value": value}
            for k, value in res_data["field_to_sum_dict"].items()
        ]
        # 排序
        res_data["field_to_sum_list"] = sorted(
            res_data["field_to_sum_list"],
            key=lambda k: k.get("value") or 0,
            reverse=True,
        )
        # 日周月
        (
            res_data["field_to_date"]["list"],
            max_min_data,
            sum_data,
            avg_data,
        ) = data_to_week_or_month(
            time_type=self.date_type,
            data=res_data["field_to_date"]["list"],
            fields=self.filed_key_list + ["total"],
        )
        res_data["field_to_date"]["max_min_sum_avg"].update(
            {
                **max_min_data,
                **sum_data,
                **avg_data,
            }
        )

    def __get_filed_key_str(self):
        filed_key_str = ""
        if not self.filed_key:
            return filed_key_str
        if isinstance(self.filed_key, list):
            filed_key_str = self.filed_key[0]
        elif isinstance(self.filed_key, str):
            filed_key_str = self.filed_key
        return filed_key_str

    def __get_page_platform(self) -> str:
        """
        获取主页平台
        :return:
        """
        platform = ""
        sql = f"SELECT page_id, network FROM social_page_info_v3 WHERE page_id = '{self.page_id}'"
        with self.db_mysql as mysql_db_:
            mysql_db_.execute(sql)
            data_info = mysql_db_.fetchone()
            if not data_info:
                return platform
            platform = PLATFORM_INT_DICT.get(data_info.get("network"))
        return platform

    def __get_es_index(self) -> str:
        """
        获取es索引
        :return:
        """
        platform_str = self.platform
        if platform_str == "vkontakte":
            platform_str = "vk"
        return f"page_posts_{platform_str}"

    def __check_params_data(self) -> None:
        """
        检查过滤字段规则格式
        :return:
        """

        required_params = {
            "date_start": self.date_start,
            "date_end": self.date_end,
            "page_id": self.page_id,
            "filed_key": self.filed_key,
            "table_name": self.table_name,
            "platform": self.platform,
            "date_source": self.date_source,
        }

        for param_name, param_value in required_params.items():
            if not param_value:
                raise OsChartsParamsError(
                    error_code="os-charts-param",
                    error_info=f"{param_name} 参数不能为空",
                )

        if self.date_source == "mysql":
            self.__check_mysql_exist()

        if self.date_source == "es":
            self.__check_es_exist()

        if self.date_type not in ["day", "week", "month"]:
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info="date_type 参数必须在此列表中 ['day', 'week', 'month']",
            )

        try:
            datetime.datetime.strptime(self.date_start, "%Y-%m-%d")
            datetime.datetime.strptime(self.date_end, "%Y-%m-%d")
        except ValueError:
            raise OsChartsParamsError(
                error_code="os-charts-param",
                error_info="date_stat/date_end 格式不正确，例子：2023-01-01",
            )

    def __check_mysql_exist(self) -> None:
        """
        mysql存在性校验
        """
        with self.db_mysql as mysql_db_:
            # 表名校验
            tables_list = list()
            mysql_db_.execute("show tables")
            for i in mysql_db_.fetchall():
                tables_list += list(i.values())
            if self.table_name not in tables_list:
                raise OsChartsParamsError(
                    error_code="os-charts-param",
                    error_info=f"table_name-{self.table_name} not in mysql db",
                )

            # 表字段校验
            if self.table_name in MIDDLE_MODEL:
                tables_field_list = list()
                mysql_db_.execute(
                    f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '{self.table_name}'"
                )
                for i in mysql_db_.fetchall():
                    tables_field_list += list(i.values())
                # 统计指标
                for filed in self.filed_key_list:
                    if filed in tables_field_list:
                        continue
                    raise OsChartsParamsError(
                        error_code="os-charts-param",
                        error_info=f"table_name-{self.table_name} not have field {filed}",
                    )
                # 过滤指标
                for filter_filed in self.filter_field.keys():
                    if filter_filed in tables_field_list:
                        continue
                    raise OsChartsParamsError(
                        error_code="os-charts-param",
                        error_info=f"table_name-{self.table_name} not have filter_filed {filter_filed}",
                    )

    def __check_es_exist(self) -> None:
        """
        es 存在性校验
        """
        with self.db_es as es_db_:
            index_mapping = es_db_.indices.get_mapping(index=self.table_name)
            if not index_mapping:
                raise ValueError(f"table_name-{self.table_name} not in es db")
            field_mapping = (
                index_mapping.get(self.table_name.replace("posts", "feed"), {})
                .get("mappings", {})
                .get("properties", {})
            )
            # 统计指标
            for filed in self.filed_key_list:
                if filed in field_mapping.keys():
                    continue
                raise OsChartsParamsError(
                    error_code="os-charts-param",
                    error_info=f"es_index_name-{self.table_name} not have field {filed}",
                )
            # 过滤指标
            for filter_filed in self.filter_field.keys():
                if filter_filed in field_mapping.keys():
                    continue
                raise OsChartsParamsError(
                    error_code="os-charts-param",
                    error_info=f"es_index_name-{self.table_name} not have filter_filed {filter_filed}",
                )

    @staticmethod
    def add_value_to_res(
        res_data: dict, date_str: str, field_key: str, value: int
    ) -> None:
        """
        组装数据
        """
        if value is None:
            return
        if date_str not in res_data["field_to_date"].keys():
            return
        if field_key not in res_data["field_to_sum"].keys():
            return
        if res_data["field_to_sum"][field_key] is None:
            res_data["field_to_sum"][field_key] = 0

        res_data["field_to_sum"][field_key] += value
        res_data["field_to_date"][date_str][field_key] = value

    @staticmethod
    def add_value_to_res_os(
        res_data: dict, date_str: str, field_key: str, value: int
    ) -> None:
        """
        组装数据 os
        """
        if value is None:
            return
        if date_str not in res_data["field_to_date"]["list"].keys():
            return
        if field_key not in res_data["field_to_sum_dict"].keys():
            return

        if res_data["field_to_date"]["list"][date_str]["total"] is None:
            res_data["field_to_date"]["list"][date_str]["total"] = 0

        if res_data["field_to_sum_dict"][field_key] is None:
            res_data["field_to_sum_dict"][field_key] = 0

        res_data["field_to_date"]["list"][date_str]["total"] += value
        res_data["field_to_date"]["list"][date_str][field_key] = value
        res_data["field_to_sum_dict"][field_key] += value


class EsChart(BaseChart):
    """
    es数据源 统计
    """

    def get_es_data(self) -> dict:
        """
        基础结构数据
        """
        res_data = self.init_res()
        query_body = self.__init_es_sql()
        with self.db_es as es_db_:
            res = es_db_.search(index=self.table_name, body=query_body)
            aggregations_res = res.get("aggregations")
            if not aggregations_res:
                return res_data
            # date add
            for bucket_data in aggregations_res.get("group_by_created_time", {}).get(
                "buckets", []
            ):
                date_str = bucket_data.get("key_as_string")
                for field_key in self.filed_key_list:
                    field_key_data = bucket_data.get(f"stats_{field_key}", {}).get(
                        self.buckets_key
                    )
                    self.add_value_to_res(
                        res_data=res_data,
                        date_str=date_str,
                        field_key=field_key,
                        value=field_key_data,
                    )
        return res_data

    def get_es_data_to_os(self) -> dict:
        """
        os 使用数据格式
        """
        res_data = self.init_res_os()
        data_info = self.get_es_data()
        for date_str, filed_data in data_info.get(f"field_to_date", {}).items():
            for field_key, value in filed_data.items():
                self.add_value_to_res_os(
                    res_data=res_data,
                    date_str=date_str,
                    field_key=field_key,
                    value=value,
                )
        self.edit_res_data_os(res_data=res_data)
        return res_data

    def __init_es_sql(self) -> dict:
        """
        生成 es query
        数据颗粒度: 按page_id 到day 级
        :return:
        """
        # query init
        query = {
            "bool": {
                "must": [],
                "must_not": [],
                "filter": [
                    {"terms": {"timeline_visibility": [1]}},
                    {
                        "range": {
                            "post_created_time": {
                                "gte": f"{self.date_start} 00:00:00",
                                "lt": f"{self.date_end} 23:59:59",
                                "time_zone": self.__edit_time_zone(),
                            }
                        }
                    },
                ],
            }
        }

        # 过滤项
        for field_key, field_data in self.filter_field.items():
            if not field_data:
                continue
            if isinstance(field_data, list):
                query["bool"]["must"].append({"terms": {field_key: field_data}})
            elif isinstance(field_data, str) or isinstance(field_data, int):
                query["bool"]["must"].append({"term": {field_key: field_data}})

        # 指标aggregations
        filed_stats = {
            f"stats_{field_key}": {"stats": {"field": field_key}}
            for field_key in self.filed_key_list
        }

        # aggregations init
        aggregations = {
            **filed_stats,
            "group_by_created_time": {
                "date_histogram": {
                    "field": "post_created_time",
                    "calendar_interval": "day",
                    "format": "yyyy-MM-dd",
                },
                "aggregations": filed_stats,
            },
        }

        query_body = {
            "track_total_hits": True,
            "query": query,
            "aggregations": aggregations,
            "size": 1,
            "from": 0,
        }
        print(f"\nquery_body--{json.dumps(query_body)}")
        return query_body

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


class MiddleChart(BaseChart):
    """
    MIDDLE_MODEL 中的数据
    """

    def get_middle_data(self) -> dict:
        """
        基础结构数据
        """
        res_data = self.init_res()
        with self.db_mysql as mysql_db_:
            mysql_db_.execute(self.__init_middle_sql())
            for data_info in mysql_db_.fetchall():
                date_str = data_info.get(self.date_field).strftime("%Y-%m-%d")
                for field_key in self.filed_key_list:
                    field_key_data = data_info.get(field_key)
                    self.add_value_to_res(
                        res_data=res_data,
                        date_str=date_str,
                        field_key=field_key,
                        value=field_key_data,
                    )
        return res_data

    def get_middle_data_to_os(self) -> dict:
        """
        os 使用数据格式
        """
        res_data = self.init_res_os()
        data_info = self.get_middle_data()
        for date_str, filed_data in data_info.get(f"field_to_date", {}).items():
            for field_key, value in filed_data.items():
                self.add_value_to_res_os(
                    res_data=res_data,
                    date_str=date_str,
                    field_key=field_key,
                    value=value,
                )
        self.edit_res_data_os(res_data=res_data)
        return res_data

    def __init_middle_sql(self) -> str:
        """
        生成中间层sql语句
        作用表: social_page_summary social_page_summary_insight
        数据粒度: 按page_id 到day 级
        :return:
        """
        sql = "SELECT "
        # 根据业务添加共有日期字段
        sql += ", ".join(self.filed_key_list + [self.date_field])
        sql += f" FROM {self.table_name}"
        if self.filter_field and isinstance(self.filter_field, dict):
            sql += " WHERE "
            # 时间过滤
            sql += f"{self.date_field} >= '{self.date_start + ' 00:00:00'}' AND "
            sql += f"{self.date_field} < '{self.date_end + ' 23:59:59'}' AND "
            for key, value in self.filter_field.items():
                if key == "page_id":
                    in_str = ""
                    if isinstance(value, list):
                        for i in value:
                            in_str += f"'{i}',"
                    else:
                        in_str = f"'{value}'"
                    in_str = in_str.strip(",")
                    sql += f"{key} IN ({in_str}) AND "
                else:
                    if isinstance(value, list):
                        sql += f"{key} IN ({', '.join(map(str, value))}) AND "
                    else:
                        sql += f"{key} = {value} AND "
            sql = sql[:-5] + ";"
        print(f"middle_sql: {sql}")
        return sql


class InsightChart(BaseChart):
    """
    insight表中的数据
    social_page_insight
    """

    def get_insight_data(self) -> dict:
        """
        基础结构数据
        """
        res_data = self.__init_insight_res()
        with self.db_mysql as mysql_db_:
            mysql_db_.execute(self.__init_insight_sql())
            for data_info in mysql_db_.fetchall():
                date_str = data_info.get("date").strftime("%Y-%m-%d")
                key = data_info.get("key")
                value = data_info.get("value")
                self.add_value_to_insight_res(
                    res_data=res_data,
                    date_str=date_str,
                    key=key,
                    value=value,
                )
        return res_data

    def get_insight_data_to_os(self) -> dict:
        """
        os 使用数据格式
        """
        res_data = self.__init_insight_res_res_os()
        data_info = self.get_insight_data()
        for date_str, filed_data in data_info.get(f"field_to_date", {}).items():
            for key, value in filed_data.items():
                self.add_value_to_insight_res_os(
                    res_data=res_data,
                    date_str=date_str,
                    key=key,
                    value=value,
                )
        self.edit_res_data_os(res_data=res_data)
        return res_data

    def __init_insight_sql(self) -> str:
        """
        生成中间层sql语句
        作用表: social_page_insight social_page_insight_linkedin
        数据粒度: 按page_id 到 date - key - value 的统计
        :return:
        """
        # 根据业务添加共有日期字段 sum字段
        sql = f"SELECT {self.table_name}.`{self.date_field}` as `date`, {self.table_name}.`{self.insight_key_name}` as `key`, SUM({self.table_name}.`value`) as `value` FROM {self.table_name}"
        # WHERE sql
        sql += " WHERE "
        # 时间过滤 校验最新一天数据字段
        if self.is_last_date:
            sql += f"`{self.date_field}` >= '{self.date_end + ' 00:00:00'}' AND "
            sql += f"`{self.date_field}` < '{self.date_end + ' 23:59:59'}' AND "
        else:
            sql += f"`{self.date_field}` >= '{self.date_start + ' 00:00:00'}' AND "
            sql += f"`{self.date_field}` < '{self.date_end + ' 23:59:59'}' AND "
        # 添加name过滤
        name_str = ""
        for i in self.filed_key_list:
            name_str += f"'{i}',"
        name_str = name_str.strip(",")
        sql += f"{self.insight_name_name} IN ({name_str}) AND "
        if self.filter_field and isinstance(self.filter_field, dict):
            for key, value in self.filter_field.items():
                if key == "page_id":
                    in_str = ""
                    if isinstance(value, list):
                        for i in value:
                            in_str += f"'{i}',"
                    else:
                        in_str = f"'{value}'"
                    in_str = in_str.strip(",")
                    sql += f"{key} IN ({in_str}) AND "
                else:
                    if isinstance(value, list):
                        sql += f"{key} IN ({', '.join(map(str, value))}) AND "
                    else:
                        sql += f"{key} = {value} AND "
        # 去除尾部and
        sql = sql[:-5]
        # GROUP BY
        sql += f" GROUP BY {self.table_name}.{self.insight_name_name}, {self.table_name}.`{self.insight_key_name}`, {self.table_name}.`{self.date_field}`"
        print(f"insight_sql: {sql}")
        return sql

    def __init_insight_res(self) -> dict:
        """
        初始化返回结构
        :return:
        """
        res_data = {
            "field_to_date": dict(),
            "field_to_sum": dict(),
        }
        date_list = get_date_list(start_date=self.date_start, end_date=self.date_end)
        for date_str in date_list:
            res_data["field_to_date"][date_str] = dict()
        return res_data

    def __init_insight_res_res_os(self) -> dict:
        """
        初始化返回结构 os
        :return:
        """
        res_data = {
            "field_to_date": {"list": dict(), "max_min_sum_avg": dict()},
            "field_to_sum_list": list(),
            "field_to_sum_dict": dict(),
        }
        date_list = get_date_list(start_date=self.date_start, end_date=self.date_end)
        for date_str in date_list:
            res_data["field_to_date"]["list"][date_str] = {"total": None}
            res_data["field_to_date"]["list"][date_str]["date"] = date_str

        return res_data

    @staticmethod
    def add_value_to_insight_res(
        res_data: dict, date_str: str, key: str, value: int
    ) -> None:
        """
        组装数据
        """
        if date_str not in res_data["field_to_date"].keys():
            return

        if key not in res_data["field_to_date"][date_str].keys():
            res_data["field_to_date"][date_str][key] = None

        if key not in res_data["field_to_sum"].keys():
            res_data["field_to_sum"][key] = None

        if value is None:
            return
        value = int(value)

        if res_data["field_to_sum"][key] is None:
            res_data["field_to_sum"][key] = 0
        if res_data["field_to_date"][date_str][key] is None:
            res_data["field_to_date"][date_str][key] = 0

        res_data["field_to_sum"][key] += value
        res_data["field_to_date"][date_str][key] += value

    @staticmethod
    def add_value_to_insight_res_os(
        res_data: dict, date_str: str, key: str, value: int
    ) -> None:
        """
        组装数据 os
        """

        if date_str not in res_data["field_to_date"]["list"].keys():
            return

        if key not in res_data["field_to_date"]["list"][date_str].keys():
            res_data["field_to_date"]["list"][date_str][key] = None

        if key not in res_data["field_to_sum_dict"].keys():
            res_data["field_to_sum_dict"][key] = None

        if value is None:
            return
        value = int(value)

        if res_data["field_to_date"]["list"][date_str]["total"] is None:
            res_data["field_to_date"]["list"][date_str]["total"] = 0

        if res_data["field_to_date"]["list"][date_str][key] is None:
            res_data["field_to_date"]["list"][date_str][key] = 0

        if res_data["field_to_sum_dict"][key] is None:
            res_data["field_to_sum_dict"][key] = 0

        res_data["field_to_date"]["list"][date_str]["total"] += value
        res_data["field_to_date"]["list"][date_str][key] += value
        res_data["field_to_sum_dict"][key] += value


class OsChart(MiddleChart, EsChart, InsightChart):
    """
    对外提供的计算类
    使用时注意事项：
    - filed_key如果为多个数据字段，那数据表、字段规则必须一致否则都以第一个字段规则为准

    """

    # 基础数据格式 入口
    @os_charts_exception
    def get_chart_data(self) -> Dict[str, Dict[str, int]]:
        """
        获取基础数据-不做日周月-不做排序等处理
        :return:
        """
        return self.__dispatch_def(source="api")

    # os 产品使用格式入口
    @os_charts_exception
    def get_chart_data_for_os(self) -> Dict[str, Dict[str, int]]:
        """
        获取os产品内数据格式
        :return:
        """
        return self.__dispatch_def()

    def __dispatch_def(self, source: str = "os") -> Dict[str, Dict[str, int]]:
        """
        进行获取函数分发
        source: os 为营销云格式
        """
        dispatch_map = {
            "os": {
                tuple(INSIGHT_MODEL): self.get_insight_data_to_os,
                tuple(MIDDLE_MODEL): self.get_middle_data_to_os,
                tuple(ES_MODEL): self.get_es_data_to_os,
            },
            "api": {
                tuple(INSIGHT_MODEL): self.get_insight_data,
                tuple(MIDDLE_MODEL): self.get_middle_data,
                tuple(ES_MODEL): self.get_es_data,
            },
        }

        if source not in dispatch_map.keys():
            raise ValueError(f"source:{source}不支持")

        for model, method in dispatch_map[source].items():
            if self.table_name in model:
                return method()
        else:
            raise ValueError(f"table_name:{self.table_name}不支持")
