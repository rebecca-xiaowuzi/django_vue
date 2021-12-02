import time
from string import Template

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
              transferdata = {}
              request_data = JSONParser().parse(request)
              if request_data['funcation']:
               Funcation=request_data.get('funcation')
              else:
               response['code'] = "9900"
               response['msg'] = "请输入函数"
               return JsonResponse(response)
              if request_data['responsetransfer']:
                responsetransfer=request_data.get('responsetransfer')
              else:
               response['code'] = "9900"
               response['msg'] = "请输入转换名称"
               return JsonResponse(response)
              "检查在执行前是否要增加参数,要增加,添加到transferdata"
              if 'requesttransfer' in request_data:
                  for k, v in request_data.get('requesttransfer').items():
                      transferdata.update({k: v})
              "直接找到函数,进行参数替换"
              tempTemplate = Template(Funcation)
              funcation = tempTemplate.substitute(transferdata)
              "执行函数"
              try:
                  result = eval(funcation)
                  "如果有值需要处理,都增加到transferdata字典中"
                  transferdata.update({responsetransfer: result})
                  response['result'] = result
                  response['transferdata'] = transferdata
                  response['code'] = "9999"
                  response['msg'] = "success"
                  return JsonResponse(response)
              except:
                  response['code'] = "9900"
                  response['msg'] = "函数不存在"
                  return JsonResponse(response)





def runfuncation(request_data):
        return eval(request_data.get("funcation"))









