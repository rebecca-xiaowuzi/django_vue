from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from api_test import models
from api_test.models import Project,User2Project
from django.db import transaction
"""项目模块"""
class addProject(View):

    def param_check(self,request_data):
        response = {}
        try:
            if not request_data['projectName'] or not request_data['projectCode']:
                response['msg'] = '参数有误'
                response['code'] = '9966'
                return JsonResponse(response)
        except:
            response['msg'] = '参数有误'
            response['code'] = '9966'
            return JsonResponse(response)

    """新增项目
      dd
      项目code不允许重复
      新增项目时选择用户,在关联表中新增关联关系
      判断用户状态是否正确且用户是否存在      
    """
    def post(self,request):
        users=[]
        request_data = JSONParser().parse(request)
        result = self.param_check(request_data=request_data)
        if result:
            return result
        response = {}
        projectCode = request_data.get('projectCode')
        projectName = request_data.get('projectName')
        projectDescription = request_data.get('projectDescription')
        users=request_data.get('users')
        try:
            models.Project.objects.get(projectCode=projectCode)
            response['code'] = '9900'
            response['msg'] = '项目已存在'
            return JsonResponse(response)
        except:
            #新增时选择了多个用户，要添加用户和项目的关联关系
            if len(users)!=0:
                #用户在用户表中是否存在且状态是不是为1
                if len(users)==models.User.objects.filter(phone__in=users).count():
                    if len(users)==models.User.objects.filter(phone__in=users).filter(status=1).count():
                        try:
                            #添加项目和关联关系 放在一个事务中
                            with transaction.atomic():
                                    for i in range(len(users)):
                                        user2project=User2Project.objects.create(phone=users[i],projectCode=projectCode)
                                        user2project.save()
                                    project = Project.objects.create(projectCode=projectCode, projectName=projectName,
                                                             projectDescription=projectDescription)
                                    project.save()
                        except Exception:
                            response['code'] = '1000'
                            response['msg'] = '系统错误'
                            return JsonResponse(response)

                    else:
                        response['code'] = '9902'
                        response['msg'] = '有用户状态为0'
                        return JsonResponse(response)
                else:
                            response['code'] = '9902'
                            response['msg'] = '有不存在的用户'
                            return JsonResponse(response)
            #新增时未选择用户，直接创建项目
            else:
                project = Project.objects.create(projectCode=projectCode, projectName=projectName, projectDescription=projectDescription)
                project.save()
            response['msg'] = 'success'
            response['code'] = '9999'
            response['projectCode'] = projectCode
            response['projectName'] = projectName
            return JsonResponse(response)