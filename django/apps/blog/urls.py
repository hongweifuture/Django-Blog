#!/usr/bin/env python3 
# coding=utf-8

"""
History:
2019/12/2 16:11 : Created by zhaohongwei 
"""

__author__ = "zhaohongwei"
__email__ = "hongweifuture@163.com"
__contact__ = "https://blog.csdn.net/z_johnny"
__version__ = "0.1"
__date__ = "2019/12/2 16:11"
__maintainer__ = "zhaohongwei,"
__description__ = "应用app内路由转发，补充项目urls.py"


from django.conf.urls import url
from .views import IndexView, AboutView, ArticleView, CategoryView, TagView, ArchivesView, BlogSearchView, TimelineView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/$', AboutView, name='about'),
    url(r'^archives/$', ArchivesView.as_view(), name='archives'),
    url(r'^article/(?P<slug>.*?)/$', ArticleView.as_view(), name='article'),
    url(r'^category/(?P<slug>.*?)/$', CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<slug>.*?)/$', TagView.as_view(), name='tag'),
    url(r'^timeline/$', TimelineView.as_view(), name='timeline'),
    url(r'^search/$', BlogSearchView.as_view(), name='search'),
]