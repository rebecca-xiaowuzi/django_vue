from django.db.models import Q
from rest_framework import serializers,validators

from api_test.models import User,Variable,Environment,ApiHead,ApiInfo,ApiRequestParam,Project,Funcation,SqlConnect,Sql,TestCase,TestCaseDetail,TestCaseSet,Project,User2Project

from django.http import request

class UserSerializer(serializers.ModelSerializer):
   """用户信息序列化"""
   phone = serializers.CharField(max_length=30,required=True)
   password = serializers.CharField(max_length=30,required=True,write_only=True)
   email = serializers.CharField(max_length=30,read_only=True)

   class Meta:
      model = User
      fields = ('id', 'phone', 'email','password')

   def validate(self,attrs):
       if User.objects.filter(phone=attrs['phone']).filter(password=attrs['password']).filter(status=1).count()==1:
          return attrs
       else:
          raise serializers.ValidationError("用户名或密码错误或者用户被禁用")


# 请求头中获取用户名称
def  getuser(request):
         user=request.META.get("HTTP_USER")
         return user


class VariableDynamicSerializer(serializers.ModelSerializer):
   """变量信息的反序列化"""
   class Meta:
      model=Variable
      fields='__all__'

   #校验项目和环境是否存在
   def validate(self,attrs):
            if  Environment.objects.filter(projectCode=attrs['projectCode']).filter(environmentName=attrs['environmentName']).count()==1:
               if  Variable.objects.filter(projectCode=attrs['projectCode']).filter(environmentName=attrs['environmentName']).filter(variableName=attrs['variableName']).count()==0:
                         return attrs
               else:
                  raise serializers.ValidationError(detail={"该变量名称在该环境下已存在"})
            raise serializers.ValidationError(detail="项目或者环境名称不存在")


class ApiInfoSerializer(serializers.ModelSerializer):
    requestParameterType = serializers.CharField( required=False)
    apiHead = serializers.JSONField(required=False)
    ApiRequestParam = serializers.JSONField(required=False)
    """接口信息序列化"""
    class Meta:
        model=ApiInfo
        fields = '__all__'
    def validate(self, attrs):
            if 'apiHead' in attrs:
                del attrs['apiHead']
            if 'ApiRequestParam' in attrs:
                del attrs['ApiRequestParam']
            """检查项目和接口是否存在"""
            if Project.objects.filter(projectCode=attrs['projectCode']).count()==1:
                if ApiInfo.objects.filter(projectCode=attrs['projectCode']).filter(apiCode=attrs['apiCode']).count()==0:
                    return attrs
                else:
                    raise serializers.ValidationError("该项目下该接口已存在")
            else:
                raise serializers.ValidationError("该项目不存在")




class ApiHeadSerializer(serializers.ModelSerializer):
    """接口请求头信息序列化"""
    class Meta:
        model=ApiHead
        fields = '__all__'

class ApiRequestParamSerializer(serializers.ModelSerializer):
    """接口请求参数信息序列化"""
    class Meta:
        model=ApiRequestParam
        fields = '__all__'


class FuncationSerializer(serializers.ModelSerializer):
    """函数信息序列化"""

    class Meta:
        model=Funcation
        fields = '__all__'

class SqlConnectSerializer(serializers.ModelSerializer):
    """数据库连接信息序列化"""

    class Meta:
        model=SqlConnect
        fields = '__all__'
        # 校验项目和环境是否存在

    def validate(self, attrs):
        if Environment.objects.filter(projectCode=attrs['projectCode']).filter(environmentName=attrs['environmentName']).count() == 1:
                return attrs
        else:
                raise serializers.ValidationError(detail="项目或者环境名称不存在")


class SqlSerializer(serializers.ModelSerializer):
    """sql信息序列化"""

    class Meta:
        model=Sql
        fields = '__all__'

class TestCaseSerializer(serializers.ModelSerializer):
    """用例信息序列化"""

    class Meta:
        model=TestCase
        fields = '__all__'

    def validate(self, attrs):
        if Project.objects.filter(projectCode=attrs['projectCode']).count() == 1:
            if TestCase.objects.filter(projectCode=attrs['projectCode']).filter(testcaseCode=attrs['testcaseCode']).count() == 0:
                return attrs
            else:
                raise serializers.ValidationError("该项目下该用例已存在")
        else:
            raise serializers.ValidationError("该项目不存在")



class TestCaseDetailSerializer(serializers.ModelSerializer):
    """用例详情信息序列化"""
    responsetransfer = serializers.CharField(required=False,write_only=True)
    requesttransfer = serializers.CharField(required=False,write_only=True)
    class Meta:
        model=TestCaseDetail
        fields = '__all__'

    def validate(self,attrs):
        if attrs['type']=='SQL':
            if Sql.objects.filter(sqlCode=attrs['testcaseDetailCode']).count()== 0:
                raise serializers.ValidationError("有sql不存在")
            else:
                return attrs
        if attrs['type']=='API':
            if ApiInfo.objects.filter(apiCode=attrs['testcaseDetailCode']).count() == 0:
               raise serializers.ValidationError("有api不存在")
            else:
                return attrs
        if attrs['type']=='TESTCASE':
            if TestCase.objects.filter(testcaseCode=attrs['testcaseDetailCode']).count() == 0:
               raise serializers.ValidationError("有用例不存在")
            else:
                return attrs
        return attrs


class TestCaseSetSerializer(serializers.ModelSerializer):
    """用例集合信息序列化"""

    class Meta:
        model=TestCaseSet
        fields = '__all__'

    def validate(self, attrs):
        if Project.objects.filter(projectCode=attrs['projectCode']).count() == 1:
            if TestCaseSet.objects.filter(Q(projectCode=attrs['projectCode']),Q(testcasesetCode=attrs['testcasesetCode'])).count() == 0:
                return attrs
            else:
                raise serializers.ValidationError("该项目下该用例集合已存在")
        else:
            raise serializers.ValidationError("该项目不存在")


class ProjectSerializer(serializers.ModelSerializer):
    """项目信息序列化"""
    users = serializers.SerializerMethodField()
    environments=serializers.SerializerMethodField()
    class Meta:
        model=Project
        fields = '__all__'
    def get_users(self,obj):
        users=User2Project.objects.filter(projectCode=obj.projectCode)
        return Project2UserSerializer(instance=users,many=True).data
    def get_environments(self,obj):
        environments=Environment.objects.filter(projectCode=obj.projectCode)
        return ProjectEnvironmentSerializer(instance=environments,many=True).data




class Project2UserSerializer(serializers.ModelSerializer):
            """项目与用户信息序列化"""
            class Meta:
                model = User2Project
                fields = ['phone','id']


class ProjectEnvironmentSerializer(serializers.ModelSerializer):
    """项目环境信息序列化"""

    class Meta:
        model = Environment
        fields = ['ip', 'environmentName']

