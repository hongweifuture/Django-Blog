from django.db import models
from django.shortcuts import reverse
# 支持markdown，富文本编译器django-mdeditor
from mdeditor.fields import MDTextField
import markdown
# django-uuslug将slug自动将中文转换为拼音
from uuslug import uuslug

class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=30, verbose_name='文章分类')
    # slug 是唯一的字段，不能出现重复 slug，所以 SlugField 的属性是 unique=True， 可设置最大值, max_length=255
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

class Tag(models.Model):
    '''
    文章标签
    '''
    name = models.CharField(max_length=30, verbose_name='文章标签')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

class Article(models.Model):
    """
    文章标题、摘要、内容、封面图片、创建时间、修改时间、分类、标签、浏览量、是否置顶
    """

    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField(
        max_length=230,
        default='文章摘要等同于网页description内容，请务必填写...',
        verbose_name='文章摘要')
    # 文章内容，使用django-mdeditor插件可实现markdown在线编辑与实时预览
    # body = models.TextField(verbose_name='文章内容')
    body = MDTextField(verbose_name='文章内容')
    # 文章默认缩略图
    img_link = models.ImageField(upload_to='images/%Y-%m', max_length=255,
                                 help_text='提示：不添加封面可以不选择图片，默认没有图片',
                                 blank=True, null=True, verbose_name='文章封面')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    category = models.ForeignKey(Category, verbose_name='文章分类')
    tags = models.ManyToManyField(Tag, verbose_name='文章标签')
    views = models.IntegerField(verbose_name='浏览量', default=0)
    is_top = models.BooleanField(verbose_name='置顶', default=False, help_text='勾选即为置顶')
    # 使用uuslug插件，自动化将标题进行拼音化分割
    slug = models.CharField(max_length=35)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

class About(models.Model):
    """
    关于
    """
    body = MDTextField(verbose_name='关于')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body


class FriendLink(models.Model):
    """
    友链
    """
    name = models.CharField(verbose_name='友链名称', max_length=50)
    description = models.CharField(verbose_name='友链描述', max_length=100, blank=True)
    link = models.URLField(verbose_name='友链地址', help_text='请填写http或https开头的完整形式地址')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_show = models.BooleanField(verbose_name='是否展示', default=True, help_text='选中表明展示')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name


class Timeline(models.Model):
    """
    时间线 From：https://github.com/Hopetree/izone/blob/master/apps/blog/models.py
    """
    COLOR_CHOICE = (
        ('primary', '基本-蓝色'),
        ('success', '成功-绿色'),
        ('info', '信息-天蓝色'),
        ('warning', '警告-橙色'),
        ('danger', '危险-红色')
    )
    SIDE_CHOICE = (
        ('L', '左边'),
        ('R', '右边'),
    )
    STAR_NUM = (
        (1, '1颗星'),
        (2, '2颗星'),
        (3, '3颗星'),
        (4, '4颗星'),
        (5, '5颗星'),
    )

    side = models.CharField(verbose_name='位置', max_length=1, choices=SIDE_CHOICE, default='L')
    star_num = models.IntegerField(verbose_name='星星个数', choices=STAR_NUM, default=3)
    icon = models.CharField(verbose_name='图标', max_length=50, default='fa fa-pencil')
    icon_color = models.CharField(verbose_name='图标颜色', max_length=20, choices=COLOR_CHOICE, default='info')
    title = models.CharField(verbose_name='标题', max_length=100)
    update_date = models.DateTimeField(verbose_name='更新时间')
    content = MDTextField(verbose_name='主要内容')

    class Meta:
        verbose_name = '时间轴'
        verbose_name_plural = verbose_name
        ordering = ['update_date']

    def __str__(self):
        return self.title[:20]

    def content_to_markdown(self):
        return markdown.markdown(self.content,
                                 extensions=['markdown.extensions.extra', ]
                                 )
