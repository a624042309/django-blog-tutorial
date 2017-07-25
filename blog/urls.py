from django.conf.urls import url
from blog import views

# 视图函数命名空间，告诉 Django 这个 urls.py 模块是属于 blog 应用的，防止与其他应用命名冲突
app_name = 'blog' 
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]