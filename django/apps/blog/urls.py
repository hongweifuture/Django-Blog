#!/usr/bin/env python3 
# coding=utf-8

"""
History:
2019/12/9 14:35 : Created by zhaohongwei 
"""

__author__ = "zhaohongwei"
__email__ = "hongweifuture@163.com"
__contact__ = "https://blog.csdn.net/z_johnny"
__version__ = "0.1"
__date__ = "2019/12/9 14:35"
__maintainer__ = "zhaohongwei,"
__description__ = "应用app内路由转发，补充项目urls.py"


from django.urls import path
from .views import IndexView, AboutView, ArticleView, CategoryView, TagView, ArchivesView, BlogSearchView, TimelineView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView, name='about'),
    path('archives/', ArchivesView.as_view(), name='archives'),
    path('article/<slug:slug>', ArticleView.as_view(), name='article'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>', TagView.as_view(), name='tag'),
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('search/', BlogSearchView.as_view(), name='search'),

]