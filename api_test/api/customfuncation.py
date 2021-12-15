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
              request_data = JSONParser().parse(request)
              return JsonResponse(runfuncation(request_data))




"""
1、根据requesttransfer将函数模板进行替换
2、函数执行的结果返回
3、返回组装后的transferdata
"""
def runfuncation(request_data):
    response = {}
    if 'transferdata' in request_data:
        transferdata = request_data.get('transferdata')
    else:
        transferdata = {}
    if 'funcation' in request_data:
        Funcation = request_data.get('funcation')
    else:
        response['code'] = "9900"
        response['msg'] = "请输入函数"
        return response
    if 'responsetransfer' in request_data:
        responsetransfer = request_data.get('responsetransfer')
    else:
        response['code'] = "9900"
        response['msg'] = "请输入转换名称"
        return response
    "检查在执行前是否要增加参数,要增加,添加到transferdata"
    if 'requesttransfer' in request_data:
        for k, v in ast.literal_eval(request_data.get('requesttransfer')).items():
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
        return response
    except:
        response['code'] = "9900"
        response['msg'] = "函数不存在"
        return response









