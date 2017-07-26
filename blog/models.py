from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

# Create your models here.
# 类名即表名,属性名即列名,自动创建ID列

# 分类
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章
class Post(models.Model):
    # 标题
    title = models.CharField(max_length=70)

    # 正文
    body = models.TextField()

    # 创建时间 & 修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 摘要 允许为空
    excerpt = models.CharField(max_length=200, blank=True)

    # 分类 & 标签
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 作者
    author = models.ForeignKey(User)

    # 阅读量 PositiveIntegerField只允许值为正整数或0
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):

        # 把kwargs参数给blog应用下的detail视图函数
        # 把文章的id(数据库中的pk) 作为详情页面的绝对地址 
        # http://127.0.0.1:8000/post/255/      /post/detail/
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 增加阅读量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 复写save 以实现提取正文前N个字符为摘要
    def save(self, *args, **kwargs):

        # 如果没有写摘要
        if not self.excerpt:

            # 首先实例化一个Markdown类,用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])

            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 84 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:80]

            # 调用父类的save方法  将数据保存到数据库中
            super(Post, self).save(*args, **kwargs)

    # 指定排序属性
    class Meta:
        ordering = ['-created_time']


        