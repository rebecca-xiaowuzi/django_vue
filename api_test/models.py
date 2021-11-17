from __future__ import unicode_literals
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone
# Create your models here.
# -*- coding: utf-8 -*-


class Book(models.Model):
    book_name = models.CharField(max_length=128)
    add_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.book_name



class User(models.Model):
    """用户表
    用户phone唯一
    """
    phone=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)


class Project(models.Model):
    """项目表
    项目code唯一
    """
    projectName=models.CharField(max_length=30)
    projectDescription=models.TextField()
    projectCode=models.CharField(max_length=30,unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)



class User2Project(models.Model):
    """
    用户与项目关系表
    电话phone与项目code对应关系：多对多
    """
    phone=models.CharField(max_length=30,verbose_name='用户电话')
    projectCode=models.CharField(max_length=30,verbose_name='项目code')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class Environment(models.Model):
    """
      环境表
    """
    ip=models.CharField(max_length=100,verbose_name='IP')
    environmentName=models.CharField(max_length=100,verbose_name='环境名称')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    projectCode = models.CharField(max_length=30,verbose_name='项目code')
    environmentDescription = models.TextField()


class Variable(models.Model):
    """
    变量表
    """
    projectCode = models.CharField(max_length=30,blank=False,verbose_name='项目code')
    environmentName = models.CharField(max_length=30, blank=False,verbose_name='环境名称')
    variableName = models.CharField(max_length=30, blank=False,verbose_name='变量名称')
    variable = models.CharField(max_length=30, blank=False,verbose_name='变量值')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=30,null=True)

HTTP_CHOICE = (
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS')
    )


REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)')
)

class ApiInfo(models.Model):
    """接口信息表"""
    projectCode = models.CharField(max_length=30, blank=False, verbose_name='项目code')
    apiCode = models.CharField(max_length=30, blank=False, verbose_name='apicode')
    apiname = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.BooleanField(default=True, verbose_name='状态')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=30, null=True)


class ApiHead(models.Model):
    """请求头信息表"""
    projectCode = models.CharField(max_length=30, blank=False, verbose_name='项目code')
    apiCode = models.CharField(max_length=30, blank=False, verbose_name='apicode')
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')
    isdefault = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=30, null=True)


class ApiRequestParam(models.Model):
    """请求参数表"""
    projectCode = models.CharField(max_length=30, blank=False, verbose_name='项目code')
    apiCode = models.CharField(max_length=30, blank=False, verbose_name='apicode')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    isdefault = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=30, null=True)


class Funcation(models.Model):
    """自定义函数表"""
    funcationName=models.CharField(max_length=30, blank=False, unique=True,verbose_name='函数名称')
    funcationCode = models.CharField(max_length=30, blank=False, unique=True,verbose_name='函数code')
    funcation=models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=30, null=True)


class SqlConnect(models.Model):
    """数据库连接信息表"""
    projectCode = models.CharField(max_length=30, blank=False, verbose_name='项目code')
    environmentName = models.CharField(max_length=30, blank=False, verbose_name='环境名称')
    sqlconnectName = models.CharField(max_length=200, blank=False, unique=True,verbose_name='sql连接名称')
    sqlconnectCode = models.CharField(max_length=200, blank=False, unique=True, verbose_name='sql连接code')
    host=models.CharField(max_length=200, blank=False, verbose_name='数据库连接地址 ')
    port=models.IntegerField(blank=False, verbose_name='数据库连接端口 ')
    username = models.CharField(max_length=200, blank=False, verbose_name='数据库连接用户名 ')
    password = models.CharField(max_length=200, blank=False, verbose_name='数据库连接地址 ')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=200, null=True)


class Sql(models.Model):
    """自定义sql表"""
    sqlName = models.CharField(max_length=200, blank=False, unique=True, verbose_name='sql名称')
    sqlCode = models.CharField(max_length=200, blank=False, unique=True, verbose_name='sqlcode')
    sql = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=200, null=True)


class TestCase(models.Model):
    """用例表"""
    projectCode = models.CharField(max_length=200, blank=False, verbose_name='项目code')
    testcaseName = models.CharField(max_length=200, blank=False, verbose_name='用例名称')
    testcaseCode = models.CharField(max_length=200, blank=False, unique=True, verbose_name='用例code')
    testcaseModel=models.CharField(max_length=200, blank=False, verbose_name='用例所属模块')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=200, null=True)

TESTCASE_CHOICE = (
    ('API', 'API'),
    ('SQL', 'SQL'),
    ('TESTCASE', 'TESTCASE'),
    ('FUNCATION', 'FUNCATION'),
    ('ASSERT', 'ASSERT')
)

class TestCaseDetail(models.Model):
    """用例与用例子元素关系表
       子元素包含 用例,sql,函数,api,断言
    """
    testcaseCode = models.CharField(max_length=200, blank=False, verbose_name='用例code,对应用例表的testcaseCode')
    testcaseDetailName = models.CharField(max_length=200, blank=False, verbose_name='用例子元素的名称')
    testcaseDetailCode = models.CharField(max_length=200, blank=False, verbose_name='用例子元素的code')
    testcaseDetailOrder = models.IntegerField( blank=False, verbose_name='用例子元素的排序')
    responsetransfer=models.CharField(max_length=500,verbose_name='response数据提取')
    requesttransfer = models.CharField(max_length=500, verbose_name='request数据替换')
    type=models.CharField(max_length=200, blank=False, verbose_name='类型',choices=TESTCASE_CHOICE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class TestCaseSet(models.Model):
    """用例集合"""
    projectCode = models.CharField(max_length=200, blank=False, verbose_name='项目code')
    testcasesetName = models.CharField(max_length=200, blank=False, verbose_name='用例集合名称')
    testcasesetCode = models.CharField(max_length=200, blank=False, unique=True, verbose_name='用例集合code')
    testcaselist = models.CharField(max_length=500,verbose_name='包含的用例id')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user = models.CharField(max_length=200, null=True)












