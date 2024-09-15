from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views import View
from rest_framework.parsers import JSONParser
from api_test import models
from api_test.models import Result
from django.http import JsonResponse
from api_test.serializers import ResultSerializer
import json


# 查询用例列表
class ResultList(View):
    def post(self, request):
        response = {}
        request_data = JSONParser().parse(request)

        kwargs = {}
        if 'projectCode' not in request_data or request_data.get('projectCode') == "":
            pass
        else:
            kwargs['projectCode__icontains'] =request_data.get("projectCode")
        if 'testcaseCode' not in request_data or request_data.get('testcaseCode') == "":
            pass
        else:
            kwargs['testcaseCode__icontains'] = request_data.get('testcaseCode')
        if 'testcasesetCode' not in request_data or request_data.get('testcasesetCode') == "":
            pass
        else:
            kwargs['testcasesetCode__icontains'] = request_data.get('testcasesetCode')

        results = Result.objects.filter(**kwargs).order_by('-id')
        total = results.count()
        # 不传page和pagesize，不分页
        if 'page' not in request_data:
            page = 1
        else:
            page = request_data.get('page')
        if 'pagesize' not in request_data:
            if total!=0:
              pagesize = total
            else:
                pagesize=1
        else:
            pagesize = request_data.get('pagesize')
        contacts = Paginator(results, pagesize)
        try:
            resultlist = contacts.page(page)
        except PageNotAnInteger:
            resultlist = contacts.page(1)
        except EmptyPage:
            resultlist = contacts.page(contacts.num_pages)
        except:
            resultlist = contacts.page(1)
        # 序列化项目信息
        data = ResultSerializer(instance=resultlist.object_list, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = total
        return JsonResponse(response)


# 查看结果详情
class GetResultDetail(View):
    def param_check(self, request_data):
        response = {}
        try:
            if not request_data["id"] :
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
        id = request_data.get('id')
        # 判断用例是否存在,查询不到就是不存在
        try:
             resultinfo=Result.objects.get(id=id)

             resultinfoSer = ResultSerializer(instance=resultinfo, many=False).data
             response['data'] = resultinfoSer
             response['msg'] = 'success'
             response['code'] = '9999'
             return JsonResponse(response)
        except :
            response['msg'] = "结果不存在"
            response['code'] = '9900'
            return JsonResponse(response)


# 断言，判断用例执行结果
#状态码要和接口文档一致
#数据库数据要正确
#  修改数据
#  增加数据
#  删除数据
#接口返回的格式要和接口文档一致
# request  需要有状态码，接口模型，数据库数据操作
# 定义期望用例执行结果是什么 接口返回结果是什么 数据库怎么操作
class TestCaseResult(View):
    def post(self, request):
        response = {}
        # request_data = JSONParser().parse(request)
        # request_data={'expe_result': '{msg: "success", code: "9999", phone: "dsdds"}',
        #               'real_result': '{msg: "success", code: "9999", phone: "dsdds"}','status_code':200}
        # #接口状态为200，继续，否则直接返回fail
        # if request_data.get('status_code') == 200:
        #       expe_result=request_data.get('expe_result')
        #       real_result=request_data.get('real_result')
        #       try:
        #           if expe_result==real_result:
        #               response['msg']='pass'
        #               return  response
        #       except json.JSONDecodeError:
        #           print('aaaaaaaaaa')
        #           response['msg'] = 'fail'
        #           return reponse
        # else:
        #     return False

