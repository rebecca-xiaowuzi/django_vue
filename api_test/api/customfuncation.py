import time

from django.db import transaction
from django.http import JsonResponse,HttpResponse
from django.views import View
from rest_framework.parsers import JSONParser
from api_test.api.login import GetUserFromHeader
from api_test.serializers import FuncationSerializer
from api_test.untils import common_funcation
"""自定义函数模块"""
class AddFuncation(View):
       def post(self,request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              funcation_serializer = FuncationSerializer(data=request_data)
              if funcation_serializer.is_valid():
                  with transaction.atomic():
                     funcation_serializer.save()
                     response['code'] = '9999'
                     response['msg'] = 'success'
                     return JsonResponse(response)
              else:
                     response['code'] = "9902"
                     response['msg'] = funcation_serializer.errors
                     return JsonResponse(response)

"""函数运行接口"""
class RunFuncation(View):
       def post(self,request):
              response = {}
              request_data = JSONParser().parse(request)
              try:
                  response['code'] = "9999"
                  response['msg'] = "success"
                  response[request_data.get("funcation")]=eval(request_data.get("funcation"))
                  return JsonResponse(response)
              except NameError as e:
                  response['code'] = "9902"
                  response['msg'] = "方法未找到"
                  return JsonResponse(response)
              except TypeError as e:
                  response['code'] = "9902"
                  response['msg'] = "参数传递错误"
                  return JsonResponse(response)



def runfuncation(request_data):
        return eval(request_data.get("funcation"))









