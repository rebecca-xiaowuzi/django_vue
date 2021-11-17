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







