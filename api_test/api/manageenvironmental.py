"""环境管理模块"""
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from api_test import models

from api_test.serializers import VariableDynamicSerializer
from api_test.api.login import GetUserFromHeader

class addEnvironment(View):
    """新增项目环境
    1、环境名不可以重复
    2、新建环境时一定要绑定项目
    """

    def param_check(self, request_data):
        response = {}
        try:
            if not request_data["ip"] or not request_data["environmentName"] or not request_data["projectCode"]:
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
        environmentName = request_data.get('environmentName')
        projectCode = request_data.get('projectCode')
        try:
            if models.Environment.objects.filter(environmentName=environmentName).count()!=0:
                response['code'] = '9900'
                response['msg'] = '该项目环境已存在'
                return JsonResponse(response)
            elif models.Project.objects.filter(projectCode=projectCode).count()==0:
                response['code'] = '9902'
                response['msg'] = '项目不存在'
                return JsonResponse(response)
            else:
                ip  = request_data.get('ip')
                environmentDescription = request_data.get('environmentDescription')
                environment = models.Environment.objects.create(environmentName=environmentName, ip=ip, projectCode=projectCode,environmentDescription=environmentDescription)
                environment.save()
                response['code'] = '9999'
                response['msg'] = 'success'
                return JsonResponse(response)
        except:
            response['msg'] = '系统错误'
            response['code'] = '9901'
            return JsonResponse(response)


class AddVariable(View):
    """新增变量
    每个项目环境下的变量名称唯一
    """

    def post(self,request):
            #获取请求头中的user
            create_user = GetUserFromHeader(request).getuser()
            response={}
            print(request)
            request_data = JSONParser().parse(request)
            request_data['create_user']=create_user
            try:
                variable_serializer=VariableDynamicSerializer(data=request_data)
                if variable_serializer.is_valid():
                    variable_serializer.save()
                    response['code'] = '9999'
                    response['msg'] = 'success'
                    response['variableName']=variable_serializer.data.get('variableName')
                    return JsonResponse(response)
                else:
                    response['code'] = "9902"
                    response['msg'] = variable_serializer.errors
                    return JsonResponse(response)
            except Exception as e:
                    response['msg'] =str(e)
                    response['code'] = "9900"
                    return JsonResponse(response)




















