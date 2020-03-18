#!/usr/bin/env python3 
# coding=utf-8

"""
History:
2019/12/2 16:13 : Created by zhaohongwei 
"""

__author__ = "zhaohongwei"
__email__ = "hongweifuture@163.com"
__contact__ = "https://blog.csdn.net/z_johnny"
__version__ = "0.1"
__date__ = "2019/12/2 16:13"
__maintainer__ = "zhaohongwei,"
__description__ = "自定义标签和过滤器，" \
                  "上级目录必须为“templatetags”，该文件名称任意，" \
                  "@register.filter：过滤器只能传两个参数，可以写在控制语句中，" \
                  "@register.simple_tag：自定义的标签可以传多个参数，不能写在控制语句中。"


from django import template
from ..models import Article, Category, Tag, FriendLink
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

# 注册自定义标签函数
register = template.Library()

#
@register.simple_tag
def get_tag_list():
    """
    获取标签的QuerySet标签对象
    :return: 返回文章所有标签
    """
    return Tag.objects.all()

@register.simple_tag
def get_category_list():
    """
    获取分类的QuerySet对象, annotate方法相比all方法会统计参数的数量
    :return: 返回文章所有分类
    """
    return Category.objects.annotate(article_num=Count('article'))

@register.simple_tag
def get_article_maxid():
    """
    获取文章最大的id，当某一id被删除，用来识别其他id
    :return: 返回文章id最大值
    """
    article_maxid = Article.objects.all().order_by('-id').first()
    return article_maxid.id

@register.simple_tag
def get_article_list():
    """
    获取文章的QuerySet对象list，sidebar.html中获取length
    :return: 返回文章列表
    """
    return Article.objects.all()

@register.simple_tag
def get_article_year(year):
    """
    获取指定年份下的所有文章
    :param year: 年份
    :return: filter指定年份的文章
    """
    return Article.objects.filter(create_date__year=year)

@register.simple_tag
def get_article_previous(article_id):
    """
    循环id判断其连续性，避免出现由于删除文章造成的id不连续，上一篇文章失败
    不能解决第一篇文章（id=1）的问题，在模板中已经解决，但由于使用slug和get_absolute_url此问题自动修复
    :param article_id: 当前文章id
    :return: 上一篇文章的QuerySet对象
    """
    has_previous = False
    id_previous = int(article_id) - 1
    while not has_previous and id_previous >= 1:
        article_previous = Article.objects.filter(id=id_previous)
        if not article_previous:
            id_previous -= 1
        else:
            has_previous = True
    if has_previous:
        article = Article.objects.filter(id=id_previous).first()
        return article
    else:
        return

@register.simple_tag
def get_article_next(article_id):
    """
    循环id判断其连续性，避免出现由于删除文章造成的id不连续，下一篇文章失败
    不能解决最后一篇文章（id=max）的问题，在模板中已经解决，但由于使用slug和get_absolute_url此问题自动修复
    :param article_id: 当前文章id
    :return: 下一篇文章的QuerySet对象
    """
    has_next = False
    id_next = int(article_id) + 1
    id_max = get_article_maxid()
    while not has_next and id_next <= id_max:
        article_next = Article.objects.filter(id=id_next).first()
        if not article_next:
            id_next += 1
        else:
            has_next = True
    if has_next:
        article = Article.objects.filter(id=id_next).first()
        return article
    else:
        return


@register.simple_tag
def get_article_top():
    """
    :return: 置顶的文章
    """
    return Article.objects.filter(top=True)


# blog.css中已经加入highlight颜色，当前为red，可自定义
#         <style>
#             span.highlighted {
#                 color: red;
#             }
#         </style>
# 不添加此方法则需要在/lib/site-packages/haystack/utils/highlighting.py中加入判断语句，约157行左右
# 否则除了关键字其他字符显示为“...”,不推荐修改源码方式
# highlighted_chunk += text[matched_so_far:]
#
# if len(self.text_block) < self.max_length:
#     return self.text_block[:start_offset] + highlighted_chunk
#
# if start_offset > 0:
#     highlighted_chunk = '...%s' % highlighted_chunk
@register.simple_tag
def search_highlight(text, q):
    """
    自定义标题搜索词高亮函数，忽略大小写
    :param text: 传入的字符
    :param q: 搜索的内容
    :return: 传入的字符和高亮的关键字
    """
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text

@register.simple_tag
def get_friendlink():
    """
    :return: 需要展示的友链连接
    """
    return FriendLink.objects.filter(is_show=True)

@register.simple_tag
def get_star(num):
    """
    时间轴显示星星
    :param num: 星星格个数
    :return: 指定个数的一排星星
    """
    timeline_star = '<i class="fa fa-star"></i>'
    return mark_safe(timeline_star * num)


@register.simple_tag
def get_star_title(num):
    """
    时间轴显示不同星星个数的说明
    :param num: 星星个数
    :return: 得到星星个数的说明，浮动显示
    """
    timeline_star_dict = {
        1: '【1颗星】：微更新，涉及轻微调整或者后期规划了内容',
        2: '【2颗星】：小更新，小幅度调整，一般不会迁移表格',
        3: '【3颗星】：中等更新，一般会增加或减少模块，有表格的迁移',
        4: '【4颗星】：大更新，涉及到应用的增减',
        5: '【5颗星】：最大程度更新，一般涉及多个应用和表格的变动',
    }
    return timeline_star_dict[num]