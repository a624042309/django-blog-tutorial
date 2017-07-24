from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):

        # 把kwargs参数给blog应用下的detail视图函数
        # 把文章的id(数据库中的pk) 作为详情页面的绝对地址 
        # http://127.0.0.1:8000/post/255/      /post/detail/
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 指定排序属性
    class Meta:
        ordering = ['-created_time']