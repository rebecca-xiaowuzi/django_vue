import json

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import View
from api_test.serializers import TestCaseSetSerializer
from rest_framework.parsers import JSONParser
from api_test.api.login import GetUserFromHeader
from api_test.models import TestCaseSet
from api_test.api.testcase import runtestcase
"""测试用例集合模块"""
class  AddTestCaseSet(View):
       "新增用例集合"
       def  post(self, request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              print(request_data)
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
            request_data = JSONParser().parse(request)
            # request_exceltestcase['create_user'] = create_user
            print(request_data)
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
                        response[testcasecode]=str(res.content)
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




























