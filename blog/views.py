from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from comments.forms import CommentForm
from blog.models import Post, Category

import markdown

# Create your views here.
# 主页
def index(request):

	post_list = Post.objects.all()
	return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章详情
# 参数pk用于接收文章id(对应models.Post下的get_absolute_url方法) 并作为url使用
def detail(request, pk):

	# 当传入的pk对应的Post在数据库存在时，返回对应的post; 不存在，返回404错误
	post = get_object_or_404(Post, pk=pk)

	# markdown
	post.body = markdown.markdown(post.body, extensions=['markdown.extensions.extra', 
														'markdown.extensions.codehilite', 
														'markdown.extensions.toc'
														])

		# 评论 表单
	form = CommentForm()
	# 获取当前 post 下的全部评论
	comment_list = post.comment_set.all()

	# 将文章、表单、评论列表 作为模板变量传给detail.html模板,以便渲染相应数据
	context = {	'post': post,
				'form': form,
				'comment_list': comment_list,
				}

	return render(request, 'blog/detail.html', context=context)


# 归档
def archives(request, year, month):
	
	post_list = Post.objects.filter(created_time__year=year, 
									created_time__month=month
									)

	return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类
def category(request, pk):

	cate = get_object_or_404(Category, pk=pk)
	post_list = Post.objects.filter(category=cate)
	return render(request, 'blog/index.html', context={'post_list': post_list})