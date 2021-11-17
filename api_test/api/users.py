from django.http import response, JsonResponse, HttpResponse
from django.views.generic import View
from api_test import models
from api_test.models import User
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from api_test.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
'''用户模块'''
class addUser(View):
           """新增用户
           1、用户名不可以重复
           2、都是必填项
           """
           def param_check(self,request_data):
               response = {}
               try:
                    if not request_data["phone"] or not request_data["email"] or not request_data["password"]:
                        response['msg'] = '参数有误'
                        response['code'] = '9966'
                        return  JsonResponse(response)

               except KeyError:
                   response['msg'] = '参数有误'
                   response['code'] = '9966'
                   return JsonResponse(response)

           def post(self, request):
              request_data=JSONParser().parse(request)
              result=self.param_check(request_data=request_data)
              if result:
                  return  result
              response = {}
              phone=request_data.get('phone')
              try:
                  models.User.objects.get(phone=phone)
                  response['code'] = '9900'
                  response['msg'] = '用户已存在'
                  return JsonResponse(response)
              except:
               password=request_data.get('password')
               email=request_data.get('email')
               user=User.objects.create(phone=phone,password=password,email=email)
               user.save()
               response['msg'] = 'success'
               response['code'] = '9999'
               response['phone']=phone
               return JsonResponse(response)

class getUsers(View):
       """查询所有用户列表"""
       def get(self,request):
        response={}
        page=request.GET.get('page')
        pagesize=request.GET.get('pagesize')
        users=models.User.objects.all().order_by('id')
        contacts =Paginator(users,int(pagesize))
        try:
          userlist=contacts.page(int(page))
        except PageNotAnInteger:
          userlist = contacts.page(1)
        except EmptyPage:
            userlist = contacts.page(contacts.num_pages)
        except:
            userlist = contacts.page(1)
        response['msg'] = 'success'
        data=UserSerializer(instance=userlist.object_list,many=True)
        response['data'] = data.data
        response['msg']='success'
        response['code']='9966'
        return JsonResponse(response)

class updateUser(View):
   """编辑用户
   1、用户名不可以修改
   2、都是必填项
   """

   def param_check(self, request_data):
       response = {}
       try:
           if not request_data["phone"] or not request_data["email"] :
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
       phone = request_data.get('phone')
       try:
           if len(models.User.objects.filter(phone=phone))!=0:
               models.User.objects.filter(phone=phone).update(email=request_data["email"],update_time=timezone.now())
               response['msg'] = 'success'
               response['code'] = '9999'
               return JsonResponse(response)
           else:
               response['code'] = '9901'
               response['msg'] = '用户不存在'
               return JsonResponse(response)
       except ObjectDoesNotExist:
           response['code'] = '9901'
           response['msg'] = '用户不存在'
           return JsonResponse(response)


class deleteUser(View):
   """删除用户
   1、用户是否存在
   2、用户名必填
   """

   def param_check(self, request_data):
       response = {}
       try:
           if not request_data["phone"] :
               response['msg'] = '参数有误ddd'
               response['code'] = '9966'
               return JsonResponse(response)

       except KeyError:
           response['msg'] = '参数有误xxxxx'
           response['code'] = '9966'
           return JsonResponse(response)

   def post(self, request):
       request_data = JSONParser().parse(request)
       result = self.param_check(request_data=request_data)
       if result:
           return result
       response = {}
       phone = request_data.get('phone')
       try:
           obj=models.User.objects.filter(phone=phone)
           if len(obj)==1:
               if  obj[0].status==1:
                   obj.update(status=0,update_time=timezone.now())
                   response['msg'] = 'update success'
                   response['code'] = '9999'
                   return JsonResponse(response)
               else:
                   response['msg'] = '该用户已删除'
                   response['code'] = '9902'
                   return JsonResponse(response)
           else:
               response['code'] = '9901'
               response['msg'] = '用户不存在'
               return JsonResponse(response)
       except ObjectDoesNotExist:
           response['code'] = '9901'
           response['msg'] = '用户不存在'
           return JsonResponse(response)







