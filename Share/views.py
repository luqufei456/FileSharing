from django.shortcuts import render
from django.views.generic import View #django的视图类
from .models import Upload
from django.http import HttpResponsePermanentRedirect, HttpResponse
import random
import string
import datetime
import json
# Create your views here.


class HomeView(View):   #定义一个类 继承django的试图类
    def get(self, request): #用于处理get请求
        context = {}
        return render(request, 'Share/base.html', context)

    def post(self, request):
        if request.FILES: #如果有文件 继续执行 没有文件的情况前端处理好了
            file = request.FILES.get('file')
            name = file.name
            size = int(file.size)
            with open('static/Share/file/'+name, 'wb') as f: #将文件写到file文件夹
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8)) #生成随机八位的code
            u = Upload(
                spath='static/Share/file/'+name,
                sname=name,
                sFilesize=size,
                scode=code,
                sPCIP=str(request.META['REMOTE_ADDR']), #获取上传文件的用户的ip
            )
            u.save() #保存到数据库
            return HttpResponsePermanentRedirect('/s/'+code) #转到展示该文件的页面


class DisplayView(View): #展现文件的视图类
    def get(self, request, scode):
        u = Upload.objects.filter(scode=str(scode)) #按scode查出所有的对象
        if u: #如果u存在 则访问次数+1 否则返回的是空 加不了
            for i in u:
                i.svisits +=1 #每次访问 次数+1
                i.save()
        context = {'content': u}
        return render(request, 'Share/content.html', context)


class MyView(View):  #定义一个用于用户管理的类
    def get(self, request):
        IP = request.META['REMOTE_ADDR']
        u = Upload.objects.filter(sPCIP=str(IP))
        for i in u:
            i.svisits += 1 #访问量+1
            i.save()
        context = {'content': u}
        return render(request, 'Share/content.html', context)


class SearchView(View):  #定义一个用于搜索的类
    def get(self, request):
        code = request.GET.get("kw") #获取请求中的kw值 搜索的内容
        u = Upload.objects.filter(sname__contains=str(code)) #查找文件名中包含搜索内容的
        print(code)
        data = {}
        if u: #当u存在
            for i in range(len(u)):  #u里有多少个 就遍历多少次 用索引取值
                u[i].svisits += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].svisits
                data[i]['filename'] = u[i].sname
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].sPCIP)
                data[i]['size'] = u[i].sFilesize
                data[i]['time'] = str(u[i].sdatetime.strftime('%Y-%m-%d %H:%M')) #将时间转换形式
                data[i]['key'] = u[i].scode
                print(data[i])
        return HttpResponse(json.dumps(data), content_type='application/json')
    # django 使用 HttpResponse 返回json 的标准方式,content_type是标准写法