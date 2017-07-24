from blog.models import Post, Category, Tag
from django import template

''' 自定义模板标签
	1.导入tamplate模块
	2.实例化template.Library类
	3.将函数get_recent_posts装饰为register.simple_tag
	ps: Django 1.9后才支持simple_tag模板标签
'''

register = template.Library()

# 最新文章模板标签  获取数据库中前num篇文章 默认5
@register.simple_tag
def get_recent_posts(num=5):

	return Post.objects.all().order_by('-created_time')[:num]


# 归档模板标签
@register.simple_tag
def archives():

	# dates方法返回一个list 元素为每篇文章的创建时间(python的date对象)，精确到月份，DESC降序
	return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
	
	return Category.objects.all()