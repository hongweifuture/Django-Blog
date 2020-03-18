#!/usr/bin/env python3 
# coding=utf-8

"""
History:
2019/12/2 16:10 : Created by zhaohongwei 
"""

__author__ = "zhaohongwei"
__email__ = "hongweifuture@163.com"
__contact__ = "https://blog.csdn.net/z_johnny"
__version__ = "0.1"
__date__ = "2019/12/2 16:10"
__maintainer__ = "zhaohongwei,"
__description__ = "自定义上下文管理器"

from django.conf import settings


def global_setting(request):
    return {
        'BLOG_ADMIN_SITE_HEADER': settings.BLOG_ADMIN_SITE_HEADER,
        'BLOG_ADMIN_SITE_TITLE': settings.BLOG_ADMIN_SITE_TITLE,
        'BLOG_ADMIN_INDEX_TITLE': settings.BLOG_ADMIN_INDEX_TITLE,
        'BLOG_HEADER_TITLE': settings.BLOG_HEADER_TITLE,
        'BLOG_HEADER_LOGO': settings.BLOG_HEADER_LOGO,
        'BLOG_SIDEBAR_TITLE': settings.BLOG_SIDEBAR_TITLE,
        'BLOG_SIDEBAR_NOTICE': settings.BLOG_SIDEBAR_NOTICE,
        'PROJECT_ON': settings.PROJECT_ON,
        'PROJECT_TITLE': settings.PROJECT_TITLE,
        'PROJECT_ARCHIVES': settings.PROJECT_ARCHIVES,
    }