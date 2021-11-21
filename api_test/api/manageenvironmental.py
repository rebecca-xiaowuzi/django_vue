"""环境管理模块"""
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from api_test import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api_test.serializers import VariableDynamicSerializer,ProjectEnvironmentSerializer
from api_test.api.login import GetUserFromHeader
from django.db.models import Q
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
                models.Environment.objects.create(environmentName=environmentName, ip=ip, projectCode=projectCode,environmentDescription=environmentDescription)
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





class updateEnvironment(View):
    """修改项目环境信息
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
                environment=models.Environment.objects.get(Q(environmentName=environmentName),Q(projectCode=projectCode))
                environment.ip  = request_data.get('ip')
                environment.environmentDescription = request_data.get('environmentDescription')
                environment.save()
                response['code'] = '9999'
                response['msg'] = 'success'
                return JsonResponse(response)
        except:
            response['msg'] = '项目或者环境不存在'
            response['code'] = '9901'
            return JsonResponse(response)

# 查看项目环境信息详情
class getEnvironmentDetail(View):

    def param_check(self, request_data):
        response = {}
        try:
            if  not request_data["environmentName"] or not request_data["projectCode"]:
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
                environment = models.Environment.objects.get(Q(environmentName=environmentName) , Q(projectCode=projectCode))
                data = ProjectEnvironmentSerializer(instance=environment, many=False)
                response['data'] = data.data
                response['msg'] = 'success'
                response['code'] = '9999'
                return JsonResponse(response)
        except  :
            response['msg'] ="项目或者环境不存在"
            response['code'] = '9901'
            return JsonResponse(response)


# 查询项目变量信息列表
class getVariablelist(View):
    def param_check(self, request_data):
        response = {}
        try:
            if  not request_data["environmentName"] or not request_data["projectCode"]:
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
        # 不传page和pagesize，默认显示第一页每页10行
        if 'page' not in  request_data:
            page=1
        else:
            page = request_data.get('page')
        if 'pagesize' not in request_data:
            pagesize=10
        else:
            pagesize =  request_data.get('pagesize')
        # //动态变量
        kwargs={}
        kwargs['environmentName']=environmentName
        kwargs['projectCode'] = projectCode
        if 'variableName' not in request_data or request_data.get('variableName') == "":
            pass
        else:
            kwargs['variableName__icontains'] = request_data.get('variableName')
        variables=models.Variable.objects.filter(**kwargs).order_by('id')
        total = variables.count()
        contacts = Paginator(variables, pagesize)
        try:
            variablelist = contacts.page(page)
        except PageNotAnInteger:
            variablelist = contacts.page(1)
        except EmptyPage:
            variablelist = contacts.page(contacts.num_pages)
        except:
            variablelist = contacts.page(1)
        # 序列化项目信息
        data = VariableDynamicSerializer(instance=variablelist, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] =total
        return JsonResponse(response)







