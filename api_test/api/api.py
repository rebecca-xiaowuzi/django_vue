import ast
import json
from string import Template

import jmespath
import  requests
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.views import View
from rest_framework.parsers import JSONParser
from api_test.serializers import ApiInfoSerializer, ApiHeadSerializer, ApiRequestParamSerializer, \
    UpdateApiInfoSerializer, ApiHeadDecSerializer, ApiRequestParamDecSerializer
from api_test.api.login import GetUserFromHeader
import requests
from api_test.models import Environment,ApiInfo,ApiHead,ApiRequestParam
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import  api_test.models
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
                 if 'apiHead' not in request_data or request_data.get('apiHead')=="":
                     pass
                 else:
                     for name  in request_data.get('apiHead'):
                             api_head['projectCode']=projectCode
                             api_head['apiCode'] = apiCode
                             api_head['create_user'] = create_user
                             api_head['name'] = name
                             api_head['value'] = request_data.get('apiHead')[name]
                             api_head['isdefault'] = 0
                             apihead_serializer = ApiHeadDecSerializer(data=api_head)
                             if apihead_serializer.is_valid():
                                apihead_serializer.save()
                             else:
                                 transaction.savepoint_rollback(save_tage)
                                 response['code'] = "9903"
                                 response['msg'] = apihead_serializer.errors
                                 return JsonResponse(response)
                 if 'ApiRequestParam' not in request_data or request_data.get('ApiRequestParam')=="":
                     pass
                 else:
                        apirequestParam['projectCode'] = projectCode
                        apirequestParam['apiCode'] = apiCode
                        apirequestParam['create_user'] = create_user
                        apirequestParam['isdefault'] = 0
                        apirequestParam['name'] = "ApiRequestParam"
                        apirequestParam['value'] = str(request_data.get('ApiRequestParam'))
                        apirequestParam_serializer = ApiRequestParamDecSerializer(data=apirequestParam)
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

# 接口调试接口
class RunApi(View):
      "接口调用调试"
      def post(self,request):
          response={}
          try:
              request_data = JSONParser().parse(request)
              jsonresponse = runApiTemplate(request_data)
              return JsonResponse(jsonresponse)
          except Exception as e:
              response['msg'] = str(e)
              response['code'] = "9901"
              return JsonResponse(response)


"""
1、根据requesttransfer将接口模板进行替换
2、接口执行的结果返回
3、返回组装后的transferdata
"""
def runApiTemplate(request_data):

    response={}
    if 'transferdata' in request_data:
     transferdata =request_data.get('transferdata')
    else:
        transferdata={}
    apicode=request_data.get('apiCode')
    projectcode = request_data.get('projectCode')
    environmentName = request_data.get('environmentName')
    "找到模板进行参数替换"
    api = ApiInfo.objects.get(Q(apiCode=apicode),Q(projectCode=projectcode))
    "检查在执行前是否要增加参数,要增加,添加到transferdata"
    if  'requesttransfer' in request_data:
        for k, v in request_data.get('requesttransfer').items():
            transferdata.update({k: v})
    apiAddress = api.apiAddress
    tempTemplate = Template(apiAddress)
    "替换后的apiaddress"
    apiAddress = tempTemplate.safe_substitute(transferdata)

    "requestType"
    requestType = api.requestType
    apiHeads = ApiHead.objects.filter(apiCode=api.apiCode).filter(projectCode=projectcode)
    if apiHeads.exists():
        apiheads = apiHeads
    else:
        "使用这个项目下的默认头信息模板"
        apiheads = ApiHead.objects.filter(apiCode='default').filter(projectCode=projectcode)
    "模板中的参数进行替换"
    apiHead = {}
    "获取到替换后的head"
    for apihead in apiheads:
        tempTemplate = Template(apihead.value)
        apiHead.update({apihead.name: tempTemplate.safe_substitute(transferdata)})
    apiRequestParams = ApiRequestParam.objects.filter(apiCode=api.apiCode).filter(
        projectCode=projectcode)
    "是否有参数"
    if apiRequestParams.exists():
        apirequestparamD = {}
        "模板中的参数进行替换"
        for apirequestparam in apiRequestParams:
            tempTemplate = Template(apirequestparam.value)
            apirequestparamD = ast.literal_eval(tempTemplate.safe_substitute(transferdata))
        "执行函数"
        request_executeapi = {'requestType': requestType, 'apiHead': apiHead,
                              'projectCode': projectcode, 'environmentName': environmentName,
                              'apiAddress': apiAddress, 'ApiRequestParam': apirequestparamD}
    else:
        request_executeapi = {'requestType': requestType, 'apiHead': apiHead,
                              'projectCode': projectcode,
                              'environmentName': environmentName, 'apiAddress': apiAddress}
    "函数执行完毕后提取结果"
    jsonresponse = runapi(request_executeapi)
    if jsonresponse.status_code==200:
       result = jsonresponse.json()
       response['response'] = jsonresponse.json()
       if jsonresponse.request.body:
         response['request_params'] = str(jsonresponse.request.body, jsonresponse.encoding)
    "如果有值需要处理,都增加到transferdata字典中"
    if 'responsetransfer' in request_data:
        "字符串转为字典"
        for k, v in request_data.get('responsetransfer').items():
            transferdata.update({k: jmespath.search(v, result)})
    response['transferdata'] = transferdata
    response['request_url'] = jsonresponse.url
    response['request_method'] = jsonresponse.request.method
    response['request_heads'] = jsonresponse.request.headers.__dict__
    response['status_code']=jsonresponse.status_code
    response['msg'] = "请求成功"
    response['code'] = "9999"
    return response




"接口执行的公共函数"
def runapi(request_data):
    method = request_data['requestType']
    head = request_data['apiHead']
    projectCode = request_data['projectCode']
    environmentName = request_data['environmentName']
    apiAddress = request_data['apiAddress']

    url = (Environment.objects.filter(projectCode=projectCode).filter(environmentName=environmentName))
    if url.exists():
        if method == 'POST':

            data = request_data['ApiRequestParam']
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


class apilist(View):
    def post(self, request):
        response = {}
        request_data = JSONParser().parse(request)
        if 'page' not in request_data:
            page = 1
        else:
            page = request_data.get('page')
        if 'pagesize' not in request_data:
            pagesize = 10
        else:
            pagesize = request_data.get('pagesize')
        kwargs = {}
        if 'projectCode' not in request_data or request_data.get('projectCode') == "":
            pass
        else:
            kwargs['projectCode__icontains'] =request_data.get("projectCode")
        if 'apiname' not in request_data or request_data.get('apiname') == "":
            pass
        else:
            kwargs['apiname__icontains'] = request_data.get('apiname')

        apis = ApiInfo.objects.filter(**kwargs).order_by('-id')
        total = apis.count()
        contacts = Paginator(apis, pagesize)
        try:
            apilist = contacts.page(page)
        except PageNotAnInteger:
            apilist = contacts.page(1)
        except EmptyPage:
            apilist = contacts.page(contacts.num_pages)
        except:
            apilist = contacts.page(1)
        # 序列化项目信息
        data = ApiInfoSerializer(instance=apilist.object_list, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = total
        return JsonResponse(response)



class getapilistByprojectcode(View):
    def get(self, request):
        response = {}
        kwargs = {}
        if not request.GET.get('projectCode'):
            pass
        else:
            kwargs['projectCode__icontains'] =request.GET.get("projectCode")
        if not request.GET.get('apiname'):
            pass
        else:
            kwargs['apiname__icontains'] = request.GET.get('apiname')

        apis = ApiInfo.objects.filter(**kwargs).order_by('-id')
        total = apis.count()
        # 序列化项目信息
        data = ApiInfoSerializer(instance=apis, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] = total
        return JsonResponse(response)




# 返回model中的请求方式等常量
class GetallType(View):
    def get(self,request):
        response = {}
        response['httpType']=api_test.models.HTTP_CHOICE
        response['requestType']=api_test.models.REQUEST_TYPE_CHOICE
        response['requestParameterType']=api_test.models.REQUEST_PARAMETER_TYPE_CHOICE
        response['msg'] = 'success'
        response['code'] = '9999'
        return JsonResponse(response)

# 查看接口详情
class GetApiDetail(View):
    def param_check(self, request_data):
        response = {}
        try:
            if not request_data["apiCode"] or not request_data["projectCode"]:
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
        apiCode = request_data.get('apiCode')
        projectCode = request_data.get('projectCode')
        # 判断api是否存在,查询不到就是不存在
        try:
             apiinfo=ApiInfo.objects.get(Q(apiCode=apiCode),Q(projectCode=projectCode))
             apiinfoSer = ApiInfoSerializer(instance=apiinfo, many=False).data
             # 判断参数是否存在,查询不到就是不存在
             try:
                  params = ApiRequestParam.objects.get(Q(apiCode=apiCode), Q(projectCode=projectCode))
                  paramSer =ast.literal_eval(ApiRequestParamSerializer(instance=params, many=False).data.get('value'))
             except:
                 # 不存在返回空字符串
                  paramSer = ''
             apiinfoSer['ApiRequestParam'] = paramSer
             heads = ApiHead.objects.filter(Q(apiCode=apiCode), Q(projectCode=projectCode))
             # 判断head是否存在，长度为0就是不存在
             if heads.count()!=0:
                 headsSer = ApiHeadSerializer(instance=heads, many=True).data

             else:
                 # 不存在返回空字符串
                 headsSer=''
             apiinfoSer['apiHead'] = headsSer
             response['data'] = apiinfoSer
             response['msg'] = 'success'
             response['code'] = '9999'
             return JsonResponse(response)
        except :
            response['msg'] = "api不存在"
            response['code'] = '9900'
            return JsonResponse(response)


class UpdateApi(View):
    """编辑api接口"""

    def post(self, request):
        api_head = {}
        apirequestParam = {}
        # 获取请求头中的user
        create_user = GetUserFromHeader(request).getuser()
        response = {}
        request_data = JSONParser().parse(request)
        request_data['create_user'] = create_user
        apiCode = request_data.get('apiCode')
        projectCode = request_data.get('projectCode')
        apiinfo=ApiInfo.objects.get(Q(projectCode=projectCode),Q(apiCode=apiCode))

        try:
            api_serializer = UpdateApiInfoSerializer(instance=apiinfo,data=request_data,many=False)
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

                if 'apiHead' not in request_data or request_data.get('apiHead') == "":

                    # 检查数据库中该接口是否有旧的参数，有的话，删除
                    apiheads=ApiHead.objects.filter(Q(projectCode=projectCode), Q(apiCode=apiCode))
                    if apiheads.count() != 0:
                        apiheads.delete()
                else:
                    # 请求中的所有的请求头的key
                    keys_request=[]
                    # 先新增和修改
                    for name in request_data.get('apiHead'):
                        api_head['projectCode'] = projectCode
                        api_head['apiCode'] = apiCode
                        api_head['create_user'] = create_user
                        api_head['name'] = name
                        api_head['value'] = request_data.get('apiHead')[name]
                        api_head['isdefault'] = 0
                        keys_request.append(name)

                        try:
                          apihead = ApiHead.objects.get(Q(projectCode=projectCode), Q(apiCode=apiCode),Q(name=name))
                          apihead_serializer = ApiHeadDecSerializer(instance=apihead,data=api_head,many=False)
                        except:
                          apihead_serializer = ApiHeadDecSerializer(data=api_head)
                        if apihead_serializer.is_valid():
                            apihead_serializer.save()
                        else:
                            transaction.savepoint_rollback(save_tage)
                            response['code'] = "9903"
                            response['msg'] = apihead_serializer.errors
                            return JsonResponse(response)
                    # 再删除掉之前的但是在本次中不存在的元素
                    # 数据库中该接口所有的name值
                    keys_database=list(ApiHead.objects.filter(Q(projectCode=projectCode), Q(apiCode=apiCode)).values_list('name',flat=True))
                    no_exits_key=[y for y in keys_database if y not in keys_request]
                    if len(no_exits_key)!=0:
                     ApiHead.objects.filter(Q(name__in=no_exits_key)).delete()

                apiparam = ApiRequestParam.objects.filter(Q(projectCode=projectCode), Q(apiCode=apiCode))
                if 'ApiRequestParam' not in request_data or request_data.get('ApiRequestParam') == "":
                    # 检查数据库中该接口是否有旧的参数，有的话，删除
                    if apiparam.count()!=0:
                        apiparam.delete()
                else:
                    apirequestParam['projectCode'] = projectCode
                    apirequestParam['apiCode'] = apiCode
                    apirequestParam['create_user'] = create_user
                    apirequestParam['isdefault'] = 0
                    apirequestParam['name'] = "ApiRequestParam"
                    apirequestParam['value'] = str(request_data.get('ApiRequestParam'))
                    if apiparam.count()!=0:
                     apirequestParam_serializer = ApiRequestParamDecSerializer(instance=apiparam[0],data=apirequestParam,many=False)
                    else:
                        apirequestParam_serializer = ApiRequestParamDecSerializer(data=apirequestParam)
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






















