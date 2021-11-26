import ast
import json

import requests
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpRequest
from django.views import View
from api_test.serializers import TestCaseSerializer,TestCaseDetailSerializer
from rest_framework.parsers import JSONParser
from api_test.api.login import GetUserFromHeader
from  api_test.models import TestCase,TestCaseDetail,ApiInfo,ApiHead,Funcation,SqlConnect,Sql,Environment,Variable,ApiRequestParam
from api_test.api.customfuncation import runfuncation
from api_test.api.customsql import excutesql
from api_test.api.api import runapi
from string import Template
import jmespath
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
        "根据用例找到用例详情,根据order排序"
        testcasedetails = TestCaseDetail.objects.filter(testcaseCode=testcaseCode).order_by('testcaseDetailOrder')
        if testcasedetails.exists():
            pass
        else:
            # 如果查不到用例详情，直接获取表单的用例详情数据
            if request_data['TestCaseDetail']:
                testcasedetails=request_data.get('TestCaseDetail')
            else:
                response['msg'] = '用例无内容'
                response['code'] = "9900"
                return JsonResponse(response)
        for testcasedetail in testcasedetails:
                "检查在执行前是否要增加参数,要增加,添加到transferdata"
                if not testcasedetail.requesttransfer == "":
                    for k, v in ast.literal_eval(testcasedetail.requesttransfer).items():
                        transferdata.update({k: v})
                if testcasedetail.type == "SQL":
                    "找到模板进行参数替换"
                    if Sql.objects.filter(sqlCode=testcasedetail.testcaseDetailCode).exists():
                        sql = Sql.objects.filter(sqlCode=testcasedetail.testcaseDetailCode)
                        sqlCode = sql.sqlCode
                        sqlconnectCode = SqlConnect.objects.get(Q(projectcode=projectcode),
                                                                Q(environmentName=environmentName)).sqlconnectCode
                        tempTemplate = Template(sql.sql)
                        sqlnew = tempTemplate.substitute(transferdata)
                        "执行sql"
                        request_executesql = {'sql': sqlnew, 'sqlCode': sqlCode, 'sqlconnectCode': sqlconnectCode}
                        "sql执行完毕后提取结果"
                        result = excutesql(request_executesql)
                        "如果有值需要处理,都增加到transferdata字典中"
                        if not testcasedetail.responsetransfer == "":
                            transferdata.update({testcasedetail.responsetransfer: result})
                        response[testcasedetail.testcaseDetailCode] = result
                    else:
                        response['msg'] = 'sql不存在'
                        response['code'] = "9900"
                        return JsonResponse(response)
                if testcasedetail.type == "FUNCATION":
                    "直接找到函数,进行参数替换"
                    tempTemplate = Template(testcasedetail.testcaseDetailCode)
                    funcation = tempTemplate.substitute(transferdata)
                    "执行函数"
                    request_executefuncation = {'funcation': funcation}
                    result = runfuncation(request_executefuncation)
                    "如果有值需要处理,都增加到transferdata字典中"
                    if not testcasedetail.responsetransfer == "":
                        transferdata.update({testcasedetail.responsetransfer: result})
                    response[testcasedetail.testcaseDetailCode] = result
                if testcasedetail.type == "API":
                    "找到模板进行参数替换"
                    if ApiInfo.objects.get(Q(apiCode=testcasedetail.testcaseDetailCode), Q(projectCode=projectcode)):
                        api = ApiInfo.objects.get(Q(apiCode=testcasedetail.testcaseDetailCode),
                                                  Q(projectCode=projectcode))
                        apiAddress = api.apiAddress
                        tempTemplate = Template(apiAddress)
                        "替换后的apiaddress"
                        apiAddress = tempTemplate.safe_substitute(transferdata)
                        "requestType"
                        requestType = api.requestType
                        apiHeads = ApiHead.objects.filter(apiCode=api.apiCode).filter(projectCode=projectcode)
                        if apiHeads.exists():
                            apiheads = apiHeads
                        else:
                            "使用这个项目下的默认头信息模板"
                            apiheads = ApiHead.objects.filter(apiCode='default').filter(projectCode=projectcode)
                        "模板中的参数进行替换"
                        apiHead = {}
                        "获取到替换后的head"
                        for apihead in apiheads:
                            tempTemplate = Template(apihead.value)
                            apiHead.update({apihead.name: tempTemplate.safe_substitute(transferdata)})
                        apiRequestParams = ApiRequestParam.objects.filter(apiCode=api.apiCode).filter(
                            projectCode=projectcode)
                        "是否有参数"
                        if apiRequestParams.exists():
                            apirequestparamD = {}
                            "模板中的参数进行替换"
                            for apirequestparam in apiRequestParams:
                                tempTemplate = Template(apirequestparam.value)
                                apirequestparamD = ast.literal_eval(tempTemplate.safe_substitute(transferdata))
                            "执行函数"
                            request_executeapi = {'requestType': requestType, 'apiHead': apiHead,
                                                  'projectCode': projectcode, 'environmentName': environmentName,
                                                  'apiAddress': apiAddress, 'ApiRequestParam': apirequestparamD}
                        else:
                            request_executeapi = {'requestType': requestType, 'apiHead': apiHead,
                                                  'projectCode': projectcode,
                                                  'environmentName': environmentName, 'apiAddress': apiAddress}
                        "函数执行完毕后提取结果"
                        jsonresponse = runapi(request_executeapi)
                        result = jsonresponse.json()
                        "如果有值需要处理,都增加到transferdata字典中"
                        if not testcasedetail.responsetransfer == "":
                            "字符串转为字典"
                            for k, v in ast.literal_eval(testcasedetail.responsetransfer).items():
                                transferdata.update({k: jmespath.search(v, result)})
                        response[testcasedetail.testcaseDetailCode] = {"请求": jsonresponse.url,
                                                                       "响应码": jsonresponse.status_code, "结果": result}

                    else:
                        response['msg'] = 'API不存在'
                        response['code'] = "9900"
                        return JsonResponse(response)

        response['msg'] = '用例执行完成'
        response['code'] = "9999"
        return JsonResponse(response)
    except Exception as e:
        response[testcasedetail.testcaseDetailCode] = {"请求": jsonresponse.url, "响应码": jsonresponse.status_code}
        response['msg'] = str(e)
        response['code'] = "9900"
        return JsonResponse(response)
































