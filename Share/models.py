from django.db import models
from datetime import datetime #导入datetime用于处理上传文件的时间字段
# Create your models here.


class Upload(models.Model):
    svisits = models.IntegerField(verbose_name=u'访问次数', default=0)  #verbose_name   指明了字段一个易于理解的名字 使用整数字段
    scode = models.CharField(max_length=8, verbose_name=u'code') #唯一标识一个文件 相当于每个文件的身份证号
    sdatetime = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间') #如果now加了括号 就是直接使用了now()方法 时间就是orm生成model的时间
    spath = models.CharField(max_length=32, verbose_name=u'下载路径')
    sname = models.CharField(max_length=32, verbose_name=u'文件名', default='')
    sFilesize = models.CharField(max_length=10, verbose_name=u'文件大小')
    sPCIP = models.CharField(max_length=32, verbose_name=u'IP地址', default='')

    class Meta:
        verbose_name = u'download'
        db_table = 'download' #声明数据表的名字 这样就不会是默认的表名了

    def __str__(self):
        return self.sname #查询时返回文件名