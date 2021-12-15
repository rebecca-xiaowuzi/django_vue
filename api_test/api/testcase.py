import ast
import json

import requests
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from django.views import View
from api_test.serializers import TestCaseSerializer,TestCaseDetailSerializer,TestCaseDetailDesSerializer
from rest_framework.parsers import JSONParser
from api_test.api.login import GetUserFromHeader
from  api_test.models import TestCase,TestCaseDetail,ApiInfo,ApiHead,Funcation,SqlConnect,Sql,Environment,Variable,ApiRequestParam
from api_test.api.customfuncation import runfuncation
from api_test.api.customsql import excutesql,runSqlTemplate
from api_test.api.api import runapi,runApiTemplate
from string import Template
import jmespath
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
"""测试用例模块"""
class  AddTestCase(View):
       "新增用例"
       def  post(self, request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              print(request_data)
              try:
                testcase_serializer = TestCaseSerializer(data=request_data)
                """放在同一个事物中"""
                with transaction.atomic():
                     save_tage = transaction.savepoint()
                     if testcase_serializer.is_valid():
                            testcase_serializer.save()
                            if 'TestCaseDetail' not in request_data:
                                response['testcaseName'] = testcase_serializer.data.get('testcaseName')
                                response['code'] = '9999'
                                response['msg'] = 'success'
                                return  JsonResponse(response)
                            else:
                                for testCaseDetails in request_data.get('TestCaseDetail'):
                                       testCaseDetails['testcaseCode']=request_data['testcaseCode']
                                       testcasedetail_serializer = TestCaseDetailSerializer(data=testCaseDetails)
                                       if testcasedetail_serializer.is_valid():
                                              testcasedetail_serializer.save()
                                       else:

                                              transaction.savepoint_rollback(save_tage)
                                              response['msg'] = testcasedetail_serializer.errors
                                              response['code'] = '9902'
                                              return JsonResponse(response)
                     else:
                           response['msg'] = testcase_serializer.errors
                           response['code'] = '9903'
                           return JsonResponse(response)
                response['testcaseName'] = testcase_serializer.data.get('testcaseName')
                response['code'] = '9999'
                response['msg'] = 'success'
                return JsonResponse(response)
              except Exception as e:
                     response['msg'] = str(e)
                     response['code'] = "9900"
                     return JsonResponse(response)





class RunTestCase(View):
    """执行用例接口
    1、根据type查询到对应的数据模板
    2、根据排序顺序运行子用例
        处理入参
        选择对应的执行接口
       处理返回值并写入对象字典中
    """
    def post(self, request):
            create_user = GetUserFromHeader(request).getuser()
            request_data = JSONParser().parse(request)
            request_data['create_user'] = create_user
            return runtestcase(request_data)


def runtestcase(request_data):
    transferdata = {}
    response = {}
    "前端传入执行在哪个环境执行哪条用例"
    projectcode = request_data.get('projectCode')
    testcaseCode = request_data.get('testcaseCode')
    environmentName = request_data.get('environmentName')
    "先获取下该项目环境下的全局变量"
    variables = Variable.objects.filter(projectCode=projectcode).filter(environmentName=environmentName)
    "queryset是否有数据，有数据，更新到transferdata"
    if variables.exists():
        for variavle in variables:
            transferdata.update({variavle.variableName: variavle.variable})
    try:
        # 直接获取表单的用例详情数据，支持未添加用例的情况下的用例执行
        if 'TestCaseDetail' in request_data:

            testcasedetails = request_data.get('TestCaseDetail')
        else:
            "根据用例找到用例详情,根据order排序"
            testcasedetails = TestCaseDetail.objects.filter(testcaseCode=testcaseCode).order_by('testcaseDetailOrder')
            if testcasedetails.exists():
                pass
            else:
                response['msg'] = '用例无内容'
                response['code'] = "9900"
                return JsonResponse(response)
        for testcasedetail in testcasedetails:
            if testcasedetail.type == "SQL":
                runsql_params={}
                "获取到sqlcode和sqlconnectcode"
                if Sql.objects.filter(sqlCode=testcasedetail.testcaseDetailCode).exists():
                    sql = Sql.objects.filter(sqlCode=testcasedetail.testcaseDetailCode)
                    sqlCode = sql.sqlCode
                    sqlconnectCode = SqlConnect.objects.get(Q(projectcode=projectcode),Q(environmentName=environmentName)).sqlconnectCode
                    runsql_params['sqlCode']=sqlCode
                    runsql_params['sqlconnectCode'] = sqlconnectCode
                else:
                    response['msg'] = 'sql不存在'
                    response['code'] = "9900"
                    return JsonResponse(response)
                if testcasedetail.requesttransfer and testcasedetail.requesttransfer!=' ':
                    requesttransfer=testcasedetail.requesttransfer
                    runsql_params['requesttransfer'] = requesttransfer
                if testcasedetail.responsetransfer and testcasedetail.responsetransfer!=' ':
                    responsetransfer=testcasedetail.responsetransfer
                    runsql_params['responsetransfer'] = responsetransfer
                runsql_params['transferdata'] = transferdata
                sql_response=runSqlTemplate(runsql_params)
                if sql_response.get('code')=='9999':
                    # 将transferdata更新
                    transferdata.update(sql_response.get('transferdata'))
                response[testcasedetail.testcaseDetailName] = sql_response
            if testcasedetail.type == "FUNCATION":
                runfuncation_params = {}
                funcation=testcasedetail.testcaseDetailCode
                runfuncation_params['funcation']=funcation
                runfuncation_params['transferdata'] = transferdata
                if testcasedetail.requesttransfer and testcasedetail.requesttransfer!=' ':
                    requesttransfer=testcasedetail.requesttransfer
                    runfuncation_params['requesttransfer'] = requesttransfer
                if testcasedetail.responsetransfer and testcasedetail.responsetransfer!=' ':
                    responsetransfer=testcasedetail.responsetransfer
                    runfuncation_params['responsetransfer'] = responsetransfer
                funcation_response=runfuncation(runfuncation_params)
                if funcation_response.get('code')=='9999':
                    # 将transferdata更新
                    transferdata.update(funcation_response.get('transferdata'))
                response[testcasedetail.testcaseDetailName] = funcation_response
            if testcasedetail.type == "API":
                runapi_params={}
                apiCode = testcasedetail.testcaseDetailCode
                runapi_params['apiCode']=apiCode
                runapi_params['transferdata'] = transferdata
                runapi_params['projectCode'] = projectcode
                runapi_params['environmentName'] = environmentName
                if testcasedetail.requesttransfer and testcasedetail.requesttransfer!=' ':
                    requesttransfer=testcasedetail.requesttransfer
                    runapi_params['requesttransfer'] = requesttransfer
                if testcasedetail.responsetransfer and testcasedetail.responsetransfer!=' ':

                    responsetransfer=testcasedetail.responsetransfer
                    runapi_params['responsetransfer'] = responsetransfer
                api_response=runApiTemplate(runapi_params)
                if api_response.get('code')=='9999':
                    # 将transferdata更新
                    transferdata.update(api_response.get('transferdata'))
                response[testcasedetail.testcaseDetailName]=api_response

        response['msg'] = '用例执行完成'
        response['code'] = "9999"
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = "9901"
        return JsonResponse(response)


# 查询用例列表
class testcaselist(View):
    def post(self, request):
        response = {}
        request_data = JSONParser().parse(request)
        if 'page' not in request_data:
            page = 1
        else:
            page = request_data.get('page')
        if 'pagesize' not in request_data:
            pagesize = 10
        else:
            pagesize = request_data.get('pagesize')
        kwargs = {}
        if 'projectCode' not in request_data or request_data.get('projectCode') == "":
            pass
        else:
            kwargs['projectCode__icontains'] =request_data.get("projectCode")
        if 'testcaseName' not in request_data or request_data.get('testcaseName') == "":
            pass
        else:
            kwargs['testcaseName__icontains'] = request_data.get('testcaseName')

        testcases = TestCase.objects.filter(**kwargs).order_by('-id')
        total = testcases.count()
        contacts = Paginator(testcases, pagesize)
        try:
            testcaselist = contacts.page(page)
        except PageNotAnInteger:
            testcaselist = contacts.page(1)
        except EmptyPage:
            testcaselist = contacts.page(contacts.num_pages)
        except:
            testcaselist = contacts.page(1)
        # 序列化项目信息
        data = TestCaseSerializer(instance=testcaselist.object_list, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = total
        return JsonResponse(response)

# 查询用例详情
# 查看接口详情
class GetTestcaseDetail(View):
    def param_check(self, request_data):
        response = {}
        try:
            if not request_data["testcaseCode"] or not request_data["projectCode"]:
                response['msg'] = '参数有误'
                response['code'] = '9966'
                return JsonResponse(response)

        except KeyError:
            response['msg'] = '参数有误'
            response['code'] = '9966'
            return JsonResponse(response)

    def post(self, request):
        request_data = JSONParser().parse(request)
        result = self.param_check(request_data=request_data)
        if result:
            return result
        response = {}
        testcaseCode = request_data.get('testcaseCode')
        projectCode = request_data.get('projectCode')
        # 判断用例是否存在,查询不到就是不存在
        try:
             testcaseinfo=TestCase.objects.get(Q(testcaseCode=testcaseCode),Q(projectCode=projectCode))

             testcaseinfoSer = TestCaseSerializer(instance=testcaseinfo, many=False).data
             testcasedetails = TestCaseDetail.objects.filter(testcaseCode=testcaseCode).order_by('testcaseDetailOrder')
             # 判断head是否存在，长度为0就是不存在
             if testcasedetails.count()!=0:
                 testcasedetailsSer = TestCaseDetailDesSerializer(instance=testcasedetails, many=True).data

             else:
                 # 不存在返回空字符串
                 testcasedetailsSer=''
             testcaseinfoSer['TestCaseDetail'] = testcasedetailsSer
             response['data'] = testcaseinfoSer
             response['msg'] = 'success'
             response['code'] = '9999'
             return JsonResponse(response)
        except :
            response['msg'] = "用例不存在"
            response['code'] = '9900'
            return JsonResponse(response)









