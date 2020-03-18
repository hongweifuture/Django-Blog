
from .models import Category, Tag, Article, About, FriendLink, Timeline
from django.contrib import admin
from django.conf import settings

admin.site.site_header = settings.BLOG_ADMIN_SITE_HEADER                   # default: "Django Administration"
admin.site.site_title = settings.BLOG_ADMIN_SITE_TITLE     # default: "Django site admin"
# admin.site.index_title = settings.BLOG_ADMIN_INDEX_TITLE                 # default: "Site administration"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')
    # admin中要求是tuple，必须加逗号，如果使用xadmin，list即可
    # fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')
    # fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_top','title', 'category', 'create_date', 'update_date')
    list_display_links = ('title',)
    # 不显示：slug，views  默认不显示create_date，update_date
    fields = ('is_top', 'title', 'summary', 'body', 'img_link', 'category', 'tags')
    list_per_page = 50  # 控制每页显示的对象数量，默认是100
    # style_fields = {'tags': 'm2m_transfer'}  # 给多选增加一个左右添加的框, 选择标签添加到右侧，对xadmin很友好
    filter_horizontal = ('tags', )  # 给多选增加一个左右添加的框, 选择标签添加到右侧，对admin很友好
    # 筛选

    search_fields = ('title',)  # 搜索
    # category是外键，筛选需要注意来约束，双下划线外键查询
    list_filter = ('is_top', 'category__name', 'create_date')
    date_hierarchy = 'update_date'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'readme', 'create_date', 'update_date')
    list_display_links = ('readme',)

    def readme(self, obj):
        return '关于自己 About 页面的内容，支持 markdown 语法，只能存在一条。'

    readme.short_description = '说明'

@admin.register(FriendLink)
class FriendlinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'link', 'create_date', 'is_show')
    list_display_links = ('name',)
    list_filter = ['name', 'is_show']

@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'side', 'update_date', 'icon', 'icon_color', 'star_num')
    # 自定义排序
    fields = ('side', ('icon', 'icon_color'), 'update_date', ('title', 'star_num'), 'content')
    # 自定义分类排序，个人设置后感觉比较丑，暂时取消
    # fieldsets = (
    #     ('图标信息', {'fields': (('icon', 'icon_color'),)}),
    #     ('时间位置', {'fields': (('side', 'update_date', 'star_num'),)}),
    #     ('主要内容', {'fields': ('title', 'content')}),
    # )
    date_hierarchy = 'update_date'
    list_filter = ('star_num', 'update_date')
