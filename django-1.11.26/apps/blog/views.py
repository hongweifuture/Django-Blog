from .models import Article, Category, Tag, About, Timeline
from django.shortcuts import get_object_or_404
from django.conf import settings
import time
# 使用 CBV（class base views），在视图里使用类处理请求
from django.shortcuts import render
# 使用 FBV（function base views），在视图里使用函数处理请求
from django.views.generic import ListView, DetailView
# 支持markdown，优化目录和瞄点
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
# django-haystack 搜索
from haystack.generic_views import SearchView
# from haystack.views import SearchView
from haystack.query import SearchQuerySet

class IndexView(ListView):
    """
        首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    # 获取数据库中的文章列表
    model = Article
    # 指定渲染使用的模板
    template_name = 'blog/index.html'
    # 上下文变量取名，变量传入到模板中
    context_object_name = 'article_index'
    # 分页，每页个数，settings.py中进行设置
    paginate_by = settings.BLOG_INDEX_PAGINATOR_BY

    # https://www.jianshu.com/p/332406309476
    # https://docs.djangoproject.com/en/1.11/topics/pagination/
    # https://www.cnblogs.com/king-lps/p/7324821.html
    # 相当于CBV中的render，向模板中传递字典
    def get_context_data(self, **kwargs):
        # 首先获得父类生成的传递给模板的字典，字典中含有 paginator、page_obj、is_paginated 三个模板变量
        context = super().get_context_data(**kwargs)

        # paginator 是 Paginator 的一个实例
        paginator = context.get('paginator')
        # page_obj 是 Page 的一个实例
        page = context.get('page_obj')
        # is_paginated 是一个布尔变量，用于表示是否已分页。不足设置的每页数量的数据， is_paginated=False
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中
        context.update(pagination_data)

        # 插入自定义的模板变量，首页滚动条，settings.py中进行设置
        context['index_marquee'] = settings.BLOG_INDEX_MARQUEE

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板
        # 记住此时字典中已有了显示分页导航条所需的数据
        return context

    def pagination_data(self, paginator, page, is_paginated):
        # 如果不足设置的每页数量的数据，则没有分页，无需显示分页导航条，不用任何分页导航条的数据返回一个空的字典
        if not is_paginated:
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 表示第一页页码后是否需要显示省略号
        left_has_more = False

        # 表示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 表示是否需要显示第一页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第一页的页码号，此时就无需再显示第一页的页码号
        # 其它情况下第一页的页码是始终需要显示的。
        first = False

        # 表示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）
            # 获取当前页右边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空）
            # 获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3)
                              if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第一页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第一页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第一页，则需要获取当前页左右两边的连续页码号
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3)
                              if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第一页和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        context = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return context

    # 返回用于queryset排序的一个或多个字段，用来进行“置顶”排序，模板中未成功实现，此方法可行
    # https://github.com/Hopetree/izone/blob/master/apps/blog/views.py
    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ('-is_top', '-create_date')


class CategoryView(IndexView):
    """
        分类页，继承自Article，只是对应Article的过滤
    """
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return super().get_queryset().filter(category=category)
        # return self.model.objects.filter(category=category)

    def get_ordering(self):
        """用来进行“置顶”排序"""
        ordering = super().get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

class TagView(IndexView):
    """
        标签页，继承自Article，只是对应Article的过滤
    """
    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return super().get_queryset().filter(tags=tag)

    def get_ordering(self):
        """用来进行“置顶”排序"""
        ordering = super().get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

class ArticleView(DetailView):
    """
        文章详情页，支持markdown
    """
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article_post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过十分钟才重新统计阅览量,作者浏览忽略
        user = self.request.user
        sessions = self.request.session
        views_key = 'views_article_{}'.format(obj.id)
        views_time = sessions.get(views_key)
        if user.id != obj.id:
            if not views_time:
                obj.increase_views()
                sessions[views_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - views_time
                if t > 60 * 10:
                    obj.increase_views()
                    sessions[views_key] = time.time()

        # 文章可以使用markdown书写，带格式的文章，像csdn写markdown文章一样
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        obj.body = md.convert(obj.body)
        # 判断文章是否有目录，模板中直接实现，下面是另外一种方法
        # m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        # obj.toc = m.group(1) if m is not None else ''
        #{% if obj.toc %}
        # https://juejin.im/post/5d5ddec4f265da038f4812ed
        obj.toc = md.toc
        return obj

class ArchivesView(ListView):
    """
        归档页面
    """
    model = Article
    template_name = 'blog/archives.html'
    context_object_name = 'article_archives'

class TimelineView(ListView):
    """
        时间轴设置，markdown转换放在models中，当前ListView类视图内实现失败
    """
    model = Timeline
    template_name = 'blog/timeline.html'
    context_object_name = 'timeline_list'

class BlogSearchView(SearchView):
    """
        搜索视图内容进行排序，实测search_indexes.py中设置不生效
    """
    template_name = 'blog/search/search.html'
    context_object_name = 'search_list'
    queryset = SearchQuerySet().order_by('-id')

def AboutView(request):
    """
    :param request:
    :return: 关于内容，添加默认值，防止body不存在而报错
    """
    body = About.objects.first()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    # body = obj.md
    if body is None:
        repo_url = 'https://github.com/hongweifuture'
        body = '<li>HONGWEI Github 地址：<a href="{}" target="_blank">{}</a></li>'.format(repo_url, repo_url)
    else:
        body = md.convert(body.body)
    return render(request, 'blog/about.html', context={'body': body})

