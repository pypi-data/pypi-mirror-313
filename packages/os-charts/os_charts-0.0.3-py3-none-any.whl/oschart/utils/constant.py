#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/4/28 5:59 PM
# @Author  : zy
# @Site    : 
# @File    : constant.py
# @Software: PyCharm
"""
文件功能:
项目相关变量
"""

FACEBOOK = 0
TWITTER = 1
INSTAGRAM = 2
LINKEDIN = 3
YOUTUBE = 4
TIKTOK = 5
VKONTAKTE = 6
WECHAT = 10
THREADS = 10

PLATFORM_DICT = {
    'facebook': FACEBOOK,
    'twitter': TWITTER,
    'instagram': INSTAGRAM,
    'linkedin': LINKEDIN,
    'youtube': YOUTUBE,
    'wechat': WECHAT,
    'tiktok': TIKTOK,
    'vkontakte': VKONTAKTE,
    'threads': THREADS,
}

PLATFORM_INT_DICT = {
    FACEBOOK: 'facebook',
    TWITTER: 'twitter',
    INSTAGRAM: 'instagram',
    LINKEDIN: 'linkedin',
    YOUTUBE: 'youtube',
    WECHAT: 'wechat',
    TIKTOK: 'tiktok',
    VKONTAKTE: 'vkontakte',
    THREADS: 'threads',
}


def platform_str_list() -> list:
    """
    pass
    """
    return list(PLATFORM_DICT.keys())
