#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 10:54 AM
# @Author  : zy
# @Site    :
# @File    : utils.py
# @Software: PyCharm
"""
文件功能:
数据处理相关工具
"""
import datetime
from typing import Tuple


def get_date_list(start_date: str, end_date: str, fmt="%Y-%m-%d"):
    """
    根据开始日期、结束日期返回这段时间里所有天的集合
    :param start_date: 开始日期(日期格式或者字符串格式)
    :param end_date: 结束日期(日期格式或者字符串格式)
    :param fmt: 格式化字符串, 如: '%Y-%m-%d'
    :return:
    """
    date_list = []
    if isinstance(start_date, str) and isinstance(end_date, str):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_list.append(start_date.strftime(fmt))
    while start_date < end_date:
        start_date += datetime.timedelta(days=1)
        date_list.append(start_date.strftime(fmt))
    return date_list


def data_to_week_or_month(
    time_type: str, data: list, fields: list, time_format="%Y-%m-%d"
) -> Tuple[list, dict, dict, dict]:
    """
    日月周切换
    :param time_type:
    :param data:
    :param fields:
    :param time_format:
    :return:
    """
    return_data = {}
    if time_type in ["week", "month"]:
        for info in data:
            if time_type == "week":
                year, week, day = datetime.datetime.strptime(
                    info["date"], time_format
                ).isocalendar()
                key = str(year) + "-" + str(week)
            else:
                key = (datetime.datetime.strptime(info["date"], time_format)).strftime(
                    "%y-%m"
                )
            if key in return_data:
                return_data[key]["date_end"] = info["date"]
                return_data[key]["date"] = (
                    return_data[key]["date_start"] + "," + return_data[key]["date_end"]
                )
                for fields_info in fields:
                    if fields_info == "fans":
                        return_data[key][fields_info] = info[fields_info]
                    else:
                        if info.get(fields_info):
                            if return_data[key][fields_info] is not None:
                                return_data[key][fields_info] += info[fields_info]
                            else:
                                return_data[key][fields_info] = info[fields_info]
            else:
                return_data[key] = {
                    "date": info["date"] + "," + info["date"],
                    "date_start": info["date"],
                    "date_end": info["date"],
                }
                for fields_info in fields:
                    return_data[key].update(
                        {
                            fields_info: info[fields_info]
                            if info.get(fields_info) is not None
                            else None
                        }
                    )
        return_data = list(return_data.values())
    else:
        return_data = data
    max_min = {}
    for i in fields:
        new_return_data = [data for data in return_data if data.get(i) is not None]
        max_item = (
            max(new_return_data, key=lambda x: 0 if not x.get(i, 0) else x.get(i, 0))
            if new_return_data
            else dict()
        )
        min_item = (
            min(new_return_data, key=lambda x: 0 if not x.get(i, 0) else x.get(i, 0))
            if new_return_data
            else dict()
        )
        max_min["max_" + i] = max_item.get(i)
        max_min["max_" + i + "_date"] = max_item.get("date")
        max_min["min_" + i] = min_item.get(i)
        max_min["min_" + i + "_date"] = min_item.get("date")
    sum_data = {f"sum_{i}": None for i in fields}
    for i in fields:
        sum_key = f"sum_{i}"
        for data in return_data:
            if data.get(i) is not None:
                if sum_data.get(sum_key) is not None:
                    sum_data[sum_key] += data.get(i)
                else:
                    sum_data[sum_key] = data.get(i)
    avg_data = {f"avg_{i}": None for i in fields}
    for i in fields:
        sum_key = f"sum_{i}"
        avg_key = f"avg_{i}"
        avg_data[avg_key] = (
            sum_data[sum_key] / len(return_data)
            if return_data and (sum_data[sum_key] is not None)
            else None
        )

    return return_data, max_min, sum_data, avg_data


if __name__ == "__main__":
    aaa = get_date_list(start_date="2021-01-01", end_date="2021-01-31")
    print(aaa)
