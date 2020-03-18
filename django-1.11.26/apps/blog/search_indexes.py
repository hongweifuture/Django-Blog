#!/usr/bin/env python3 
# coding=utf-8

"""
History:
2019/12/2 16:03 : Created by zhaohongwei 
"""

__author__ = "zhaohongwei"
__email__ = "hongweifuture@163.com"
__contact__ = "https://blog.csdn.net/z_johnny"
__version__ = "0.1"
__date__ = "2019/12/2 16:03"
__maintainer__ = "zhaohongwei,"
__description__ = "django-haystack 必要配置文件"

from haystack import indexes
from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # 一般来说，text: 索引字段。document=True: 指定该text为索引字段。
    # use_template=True 指定对表中的哪些字段进行关键词分析，建立索引文件，对字段的说明说明后续我们还要指定一个模板文件。
    # template_name：指定模板文件，可不指定，默认为 template_name="search/indexes/APP名字/APP名字小写_text.txt"
    text = indexes.CharField(document=True, use_template=True, template_name="blog/search/Article_text.txt")

    def get_model(self):
        # 返回 需要检索的 模型类
        return Article

    # queryset返回所有，若指定排序请在views中进行指定，当前设置测试不生效
    def index_queryset(self, using=None):
        return self.get_model().objects.all()


