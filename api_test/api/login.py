from django.http import JsonResponse,request
from django.views import View
from rest_framework.parsers import JSONParser
from api_test.serializers import UserSerializer

"""登录"""
class Login(View):

       def post(self,request):
           response = {}
           request_data = JSONParser().parse(request)
           try:
               user_serializer = UserSerializer(data=request_data)
               if user_serializer.is_valid():
                   response['phone']=user_serializer.data.get('phone')
                   response['code'] = '9999'
                   response['msg'] = 'success'
                   return JsonResponse(response)
               else:
                   response['code'] = "9902"
                   response['msg'] = user_serializer.errors
                   return JsonResponse(response)
           except Exception as e:
               response['msg'] = str(e)
               response['code'] = "9900"
               return JsonResponse(response)



"""获取请求头部的用户名"""
class GetUserFromHeader:
    def __init__(self,request_data:request):
        self.request_data=request_data
    #获取请求头中的信息并且校验(暂未实现校验)
    def  getuser(self):
         user=self.request_data.META.get("HTTP_USER")
         return user


if __name__=='__main__':
    a= request()
    b=GetUserFromHeader(a)
    print(b.getuser())