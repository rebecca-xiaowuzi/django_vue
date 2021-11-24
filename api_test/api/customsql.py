from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser
from api_test.serializers import SqlConnectSerializer,SqlSerializer
from api_test.api.login import GetUserFromHeader
from api_test.models import SqlConnect,Sql
import pymysql
"""sql模块"""

class  AddSqlConnect(View):
       "新增数据库连接信息"
       def  post(self,request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              try:
                     sqlconnect_serializer = SqlConnectSerializer(data=request_data)
                     if sqlconnect_serializer.is_valid():
                            sqlconnect_serializer.save()
                            response['sqlname'] = sqlconnect_serializer.data.get('sqlconnectName')
                            response['code'] = '9999'
                            response['msg'] = 'success'
                            return JsonResponse(response)
                     else:
                            response['code'] = "9902"
                            response['msg'] = sqlconnect_serializer.errors
                            return JsonResponse(response)
              except Exception as e:
                     response['msg'] = str(e)
                     response['code'] = "9900"
                     return JsonResponse(response)


# 查询项目数据量连接信息列表
class getsqlconnectlist(View):
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
        if 'sqlconnectName' not in request_data or request_data.get('sqlconnectName') == "":
            pass
        else:
            kwargs['sqlconnectName__icontains'] = request_data.get('sqlconnectName')
        sqlconnects=SqlConnect.objects.filter(**kwargs).order_by('-id')
        total = sqlconnects.count()
        contacts = Paginator(sqlconnects, pagesize)
        try:
            sqlconnectlist = contacts.page(page)
        except PageNotAnInteger:
            sqlconnectlist = contacts.page(1)
        except EmptyPage:
            sqlconnectlist = contacts.page(contacts.num_pages)
        except:
            sqlconnectlist = contacts.page(1)
        # 序列化连接信息
        data = SqlConnectSerializer(instance=sqlconnectlist, many=True)
        response['data'] = data.data
        response['msg'] = 'success'
        response['code'] = '9999'
        response['total'] =total
        return JsonResponse(response)

# 查询连接信息详情
class getsqlconnectDetail(View):
    def param_check(self, request_data):
        response = {}
        try:
            if not request_data["sqlconnectCode"] or not request_data["projectCode"] or not request_data["environmentName"]:
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
        sqlconnectCode = request_data.get('sqlconnectCode')
        projectCode = request_data.get('projectCode')
        environmentName = request_data.get('environmentName')
        # 判断数据是否存在,查询不到就是不存在
        try:
             sqlconnectinfo=SqlConnect.objects.get(Q(sqlconnectCode=sqlconnectCode),Q(projectCode=projectCode),Q(environmentName=environmentName))
             sqlconnectinfoSer = SqlConnectSerializer(instance=sqlconnectinfo, many=False).data
             response['data'] = sqlconnectinfoSer
             response['msg'] = 'success'
             response['code'] = '9999'
             return JsonResponse(response)
        except :
            response['msg'] = "连接信息不存在"
            response['code'] = '9999'
            return JsonResponse(response)

#修改连接信息
class UpdateSqlConnect(View):
    def post(self, request):
        create_user = GetUserFromHeader(request).getuser()
        response = {}
        request_data = JSONParser().parse(request)
        request_data['create_user'] = create_user
        environmentName = request_data.get('environmentName')
        projectCode = request_data.get('projectCode')
        sqlconnectCode = request_data.get('sqlconnectCode')
        try:
            sqlconnectinfo = SqlConnect.objects.get(Q(projectCode=projectCode), Q(environmentName=environmentName),
                                                    Q(sqlconnectCode=sqlconnectCode))
            sqlconnectinfo.port=request_data.get('port')
            sqlconnectinfo.host=request_data.get('host')
            sqlconnectinfo.username=request_data.get('username')
            sqlconnectinfo.password=request_data.get('password')
            sqlconnectinfo.save()

            response['code'] = '9999'
            response['msg'] = 'success'
            return JsonResponse(response)
        except Exception as e:
              response['msg'] = str(e)
              response['code'] = "9900"
              return JsonResponse(response)



class AddSql(View):
       "新增sql"
       def post(self,request):
              create_user = GetUserFromHeader(request).getuser()
              response = {}
              request_data = JSONParser().parse(request)
              request_data['create_user'] = create_user
              try:
                     sql_serializer = SqlSerializer(data=request_data)
                     if sql_serializer.is_valid():
                            sql_serializer.save()
                            response['sqlname'] = sql_serializer.data.get('sqlName')
                            response['code'] = '9999'
                            response['msg'] = 'success'
                            return JsonResponse(response)
                     else:
                            response['code'] = "9902"
                            response['msg'] = sql_serializer.errors
                            return JsonResponse(response)
              except Exception as e:
                     response['msg'] = str(e)
                     response['code'] = "9900"
                     return JsonResponse(response)



class ExcuteSql(View):
       "运行sql"
       def post(self, request):
              response = {}
              request_data = JSONParser().parse(request)
              try:
                     sqlconnectCode=request_data.get('sqlconnectCode')
                     c=SqlConnect.objects.get(sqlconnectCode=sqlconnectCode)
                     host=c.host
                     port=c.port
                     user=c.username
                     passwd=c.password
                     sql=request_data.get('sql')
                     connect=pymysql.connect(host=host,port=port,user=user,password=passwd,charset="utf8")
                     cursor = connect.cursor()
                     cursor.execute(sql)
                     data=cursor.fetchall()
                     cursor.close()
                     connect.close()
                     response['values'] = data
                     response['code'] = '9999'
                     response['msg'] = 'success'
                     return JsonResponse(response)
              except Exception as e:
                     response['code'] = '9900'
                     response['msg'] = str(e)



def excutesql(request_data):
       response={}
       try:
              sqlconnectCode = request_data.get('sqlconnectCode')
              c = SqlConnect.objects.get(sqlconnectCode=sqlconnectCode)
              host = c.host
              port = c.port
              user = c.username
              passwd = c.password
              sql = request_data.get('sql')
              connect = pymysql.connect(host=host, port=port, user=user, password=passwd, charset="utf8")
              cursor = connect.cursor()
              cursor.execute(sql)
              data = cursor.fetchall()
              cursor.close()
              connect.close()
              return data
       except Exception as e:
              response['code'] = '9900'
              response['msg'] = str(e)







