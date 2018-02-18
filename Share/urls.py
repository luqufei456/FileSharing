from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),#引用视图对象的时候调用对象的as_view()方法,
    #这个时候是以对象的形式调用,必须要加括号,而不能使用 as_view
    url(r'^s/(?P<scode>\d+)$', views.DisplayView.as_view()),
    url(r'^my/$', views.MyView.as_view(), name='MY'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),

]