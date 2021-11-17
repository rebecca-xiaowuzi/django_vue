import json

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.views import View
from rest_framework.parsers import JSONParser
from api_test.serializers import ApiInfoSerializer,ApiHeadSerializer,ApiRequestParamSerializer
from api_test.api.login import GetUserFromHeader
import requests
from api_test.models import Environment
class AddApi(View):
     """新增api接口"""
     def post(self,request):
         api_head={}
         apirequestParam={}
         # 获取请求头中的user
         create_user = GetUserFromHeader(request).getuser()
         response = {}
         request_data = JSONParser().parse(request)
         request_data['create_user'] = create_user
         apiCode=request_data.get('apiCode')
         projectCode = request_data.get('projectCode')
         try:

             api_serializer = ApiInfoSerializer(data=request_data)
             """放在同一个事物中"""
             with transaction.atomic():
                 save_tage = transaction.savepoint()
                 if api_serializer.is_valid():
                    api_serializer.save()
                 else:
                     transaction.savepoint_rollback(save_tage)
                     response['code'] = "9902"
                     response['msg'] = api_serializer.errors
                     return JsonResponse(response)
                 if 'apiHead' not in request_data:
                     response['apiCode'] = api_serializer.data.get('apiCode')
                     response['apiname'] = api_serializer.data.get('apiname')
                     response['code'] = '9999'
                     response['msg'] = 'success'
                     return JsonResponse(response)
                     return
                 else:
                     for name  in request_data.get('apiHead'):
                             api_head['projectCode']=projectCode
                             api_head['apiCode'] = apiCode
                             api_head['create_user'] = create_user
                             api_head['name'] = name
                             api_head['value'] = request_data.get('apiHead')[name]
                             api_head['isdefault'] = 0
                             apihead_serializer = ApiHeadSerializer(data=api_head)
                             if apihead_serializer.is_valid():
                                apihead_serializer.save()
                             else:
                                 transaction.savepoint_rollback(save_tage)
                                 response['code'] = "9903"
                                 response['msg'] = apihead_serializer.errors
                                 return JsonResponse(response)
                 if 'ApiRequestParam' not in request_data:
                     response['apiCode'] = api_serializer.data.get('apiCode')
                     response['apiname'] = api_serializer.data.get('apiname')
                     response['code'] = '9999'
                     response['msg'] = 'success'
                     return JsonResponse(response)
                 else:
                        apirequestParam['projectCode'] = projectCode
                        apirequestParam['apiCode'] = apiCode
                        apirequestParam['create_user'] = create_user
                        apirequestParam['isdefault'] = 0
                        apirequestParam['name'] = "ApiRequestParam"
                        apirequestParam['value'] = str(request_data.get('ApiRequestParam'))
                        apirequestParam_serializer = ApiRequestParamSerializer(data=apirequestParam)
                        if apirequestParam_serializer.is_valid():
                          apirequestParam_serializer.save()
                        else:
                            transaction.savepoint_rollback(save_tage)
                            response['code'] = "9904"
                            response['msg'] = apirequestParam_serializer.errors
                            return JsonResponse(response)

             response['apiCode'] = api_serializer.data.get('apiCode')
             response['apiname'] = api_serializer.data.get('apiname')
             response['code'] = '9999'
             response['msg'] = 'success'
             return JsonResponse(response)
         except Exception as e:
             transaction.savepoint_rollback(save_tage)
             response['msg'] = str(e)
             response['code'] = "9900"
             return JsonResponse(response)

class RunApi(View):
      "接口调用调试"
      def post(self,request):
          request_data = JSONParser().parse(request)
          return request_data


"接口执行的公共函数"
def runapi(request_data):
    method = request_data['requestType']
    head = request_data['apiHead']
    projectCode = request_data['projectCode']
    environmentName = request_data['environmentName']
    apiAddress = request_data['apiAddress']
    url = (Environment.objects.filter(projectCode=projectCode).filter(environmentName=environmentName))
    if method == 'POST':
        data = request_data['ApiRequestParam']
        print(type(data))
        r = requests.request("POST", url[0].ip + apiAddress, json=data, headers=head)
        return r
    if method == 'GET':
        if 'ApiRequestParam'  in request_data:
            param = request_data['ApiRequestParam']
            r = requests.request("GET", url[0].ip + apiAddress, param=param, headers=head)
            return r
        else:
            r = requests.request("GET", url[0].ip + apiAddress, headers=head)
            return r
































