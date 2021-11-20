from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from api_test import models
from api_test.models import Project,User2Project
from django.db import transaction

from api_test.serializers import ProjectSerializer

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
        print(projectCode)
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
                                       User2Project.objects.create(phone=users[i],projectCode=projectCode)
                                    Project.objects.create(projectCode=projectCode, projectName=projectName,projectDescription=projectDescription)
                        except Exception as e:
                            response['code'] = '1000'
                            response['msg'] = e
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
                Project.objects.create(projectCode=projectCode, projectName=projectName, projectDescription=projectDescription)

            response['msg'] = 'success'
            response['code'] = '9999'
            response['projectCode'] = projectCode
            response['projectName'] = projectName
            return JsonResponse(response)


class getProjects(View):
    """查询所有项目列表"""

    def get(self, request):
        response = {}
        page = request.GET.get('page')
        pagesize = request.GET.get('pagesize')
        projects = models.Project.objects.all().order_by('id')
        contacts = Paginator(projects, int(pagesize))
        try:
            projectlist = contacts.page(int(page))
        except PageNotAnInteger:
            projectlist = contacts.page(1)
        except EmptyPage:
            projectlist = contacts.page(contacts.num_pages)
        except:
            projectlist = contacts.page(1)
        # 序列化项目信息
        data = ProjectSerializer(instance=projectlist.object_list, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = models.Project.objects.all().count()
        return JsonResponse(response)


class updateProject(View):
   """编辑项目信息
   """

   def param_check(self, request_data):
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

   """编辑项目
     dd
     项目code不允许修改
     新增项目时选择用户,在关联表中新增关联关系
     判断用户状态是否正确且用户是否存在      
   """

   def post(self, request):
       users = []
       request_data = JSONParser().parse(request)
       result = self.param_check(request_data=request_data)
       if result:
           return result
       response = {}
       projectCode = request_data.get('projectCode')
       projectName = request_data.get('projectName')
       projectDescription = request_data.get('projectDescription')
       users = request_data.get('users')
       try:
           models.Project.objects.get(projectCode=projectCode)
           # 编辑时选择了多个用户，要修改用户和项目的关联关系
           if len(users) != 0:
               # 用户在用户表中是否存在且状态是不是为1
               if len(users) == models.User.objects.filter(phone__in=users).count():
                   if len(users) == models.User.objects.filter(phone__in=users).filter(status=1).count():
                       try:
                           # 添加项目和关联关系 放在一个事务中
                           with transaction.atomic():
                               # 删除之前的绑定关系
                               User2Project.objects.filter(projectCode=projectCode).delete()
                               # 新增新的绑定关系
                               for i in range(len(users)):
                                   User2Project.objects.create(phone=users[i],projectCode=projectCode)
                               # 修改项目相关信息
                               project = Project.objects.get(projectCode=projectCode)
                               project.projectName=projectName
                               project.projectDescription=projectDescription
                               project.save()
                       except :
                           response['code'] = '1000'
                           response['msg'] = "系统错误"
                           return JsonResponse(response)

                   else:
                       response['code'] = '9902'
                       response['msg'] = '有用户状态为0'
                       return JsonResponse(response)
               else:
                   response['code'] = '9902'
                   response['msg'] = '有不存在的用户'
                   return JsonResponse(response)
           # 修改时删除用户，直接修改项目并且删除绑定关系
           else:
               # 修改项目相关信息
               project = Project.objects.get(projectCode=projectCode)
               project.projectName = projectName
               project.projectDescription = projectDescription
               project.save()
               # 之前有绑定信息，直接删除信息
               if User2Project.objects.filter(projectCode=projectCode).count()!=0:
                   User2Project.objects.filter(projectCode=projectCode).delete()
           response['msg'] = 'success'
           response['code'] = '9999'
           response['projectCode'] = projectCode
           response['projectName'] = projectName
           return JsonResponse(response)
       except:
           response['code'] = '9900'
           response['msg'] = "项目不存在"
           return JsonResponse(response)