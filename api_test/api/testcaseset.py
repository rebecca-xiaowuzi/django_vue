import json

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import View
from api_test.serializers import TestCaseSetSerializer,ResultSerializer
from rest_framework.parsers import JSONParser
from api_test.api.login import GetUserFromHeader
from api_test.models import TestCaseSet,Result
from api_test.api.testcase import runtestcase
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
"""测试用例集合模块"""
class  AddTestCaseSet(View):
       "新增用例集合"
       def  post(self, request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              try:
                testcaseset_serializer = TestCaseSetSerializer(data=request_data)
                if testcaseset_serializer.is_valid():
                            testcaseset_serializer.save()
                            response['testcasesetName'] = testcaseset_serializer.data.get('testcasesetName')
                            response['code'] = '9999'
                            response['msg'] = 'success'
                            return JsonResponse(response)
                else:
                           response['msg'] = testcaseset_serializer.errors
                           response['code'] = '9903'
                           return JsonResponse(response)
                return JsonResponse(response)
              except Exception as e:
                     response['msg'] = str(e)
                     response['code'] = "9900"
                     return JsonResponse(response)

class  RunTestCaseSet(View):
        "运行用例集合"
        def post(self, request):
            create_user = GetUserFromHeader(request).getuser()
            response = {}
            request_exceltestcase={}
            result_data={}
            request_data = JSONParser().parse(request)
            # request_exceltestcase['create_user'] = create_user
            testcasesetCode=request_data['testcasesetCode']
            request_exceltestcase['projectCode']=request_data['projectCode']
            request_exceltestcase['environmentName'] = request_data['environmentName']
            try:
                testcaseset=TestCaseSet.objects.get(Q(projectCode=request_data['projectCode']),Q(testcasesetCode=testcasesetCode))
                if not testcaseset.testcaselist == "":
                    testcasecodes=testcaseset.testcaselist.replace("[","").replace("]","").split(",")
                    for testcasecode in testcasecodes:
                        request_exceltestcase['testcaseCode']=testcasecode
                        res=runtestcase(request_exceltestcase)
                        response[testcasecode]=res
                    # 将用例执行的结果写入到reslut表中
                    result_data['create_user'] = create_user
                    result_data['projectCode'] = request_data.get('projectCode')
                    result_data['testcasesetCode'] = testcasesetCode
                    result_data['request'] = str(request_data)
                    result_data['result_detail'] = str(response)
                    Result_serializer = ResultSerializer(data=result_data)
                    if Result_serializer.is_valid():
                        Result_serializer.save()
                    else:
                        response['code'] = "9902"
                        response['msg'] = Result_serializer.errors
                        return JsonResponse(response)
                    response['msg'] = "用例集执行完成"
                    response['code'] = "9999"
                    return JsonResponse(response)
                else:
                    response['msg'] = "用例集合未添加用例"
                    response['code'] = "9900"
                    return JsonResponse(response)

            except NameError:
              response['msg'] ="用例集合不存在"
              response['code'] = "9900"
              return JsonResponse(response)



# 查询用例集合列表
class testcasesetlist(View):
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
        if 'testcasesetName' not in request_data or request_data.get('testcasesetName') == "":
            pass
        else:
            kwargs['testcasesetName__icontains'] = request_data.get('testcasesetName')

        testcasesets = TestCaseSet.objects.filter(**kwargs).order_by('-id')
        total = testcasesets.count()
        contacts = Paginator(testcasesets, pagesize)
        try:
            testcasesetlist = contacts.page(page)
        except PageNotAnInteger:
            testcasesetlist = contacts.page(1)
        except EmptyPage:
            testcasesetlist = contacts.page(contacts.num_pages)
        except:
            testcasesetlist = contacts.page(1)
        # 序列化项目信息
        data = TestCaseSetSerializer(instance=testcasesetlist.object_list, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = total
        return JsonResponse(response)
























