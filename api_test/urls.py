from django.conf.urls import url

from .api import users, project,manageenvironmental,login,api,customfuncation,customsql,testcase,testcaseset
from api_test.api.views import *


urlpatterns = [
    url(r'add_book$', add_book, ),
    url(r'show_books$', show_books, ),
    url(r'User/addUser', users.addUser.as_view()),
    url(r'User/getUsers', users.getUsers.as_view()),
    url(r'User/updateUser', users.updateUser.as_view()),
    url(r'User/deleteUser', users.deleteUser.as_view()),
    url(r'Project/addProject', project.addProject.as_view()),
    url(r'Project/getProjects', project.getProjects.as_view()),
    url(r'Project/updateProject', project.updateProject.as_view()),
    url(r'Environment/addEnvironment', manageenvironmental.addEnvironment.as_view()),
url(r'Environment/updateEnvironment', manageenvironmental.updateEnvironment.as_view()),
url(r'Environment/getEnvironmentDetail', manageenvironmental.getEnvironmentDetail.as_view()),
url(r'Environment/getEnvironmentbyprojectcode', manageenvironmental.getEnvironmentbyprojectcode.as_view()),
    url(r'Environment/addVariable', manageenvironmental.AddVariable.as_view()),
    url(r'Environment/getVariablelist', manageenvironmental.getVariablelist.as_view()),
    url(r'Login/login', login.Login.as_view()),
    url(r'Api/addApi', api.AddApi.as_view()),
url(r'Api/UpdateApi', api.UpdateApi.as_view()),
url(r'Api/GetApiDetail', api.GetApiDetail.as_view()),
url(r'Api/getallType', api.GetallType.as_view()),
url(r'Api/apilist', api.apilist.as_view()),
    url(r'Api/runApi', api.RunApi.as_view()),
    url(r'Funcation/addFuncation', customfuncation.AddFuncation.as_view()),
    url(r'Funcation/runFuncation', customfuncation.RunFuncation.as_view()),
    url(r'Sql/AddSqlConnect', customsql.AddSqlConnect.as_view()),
    url(r'Sql/AddSql', customsql.AddSql.as_view()),
    url(r'Sql/ExcuteSql', customsql.ExcuteSql.as_view()),
    url(r'TestCase/AddTestCase', testcase.AddTestCase.as_view()),
    url(r'TestCase/runTestCase', testcase.RunTestCase.as_view()),
    url(r'TestCaseSet/AddTestCaseSet', testcaseset.AddTestCaseSet.as_view()),
    url(r'TestCaseSet/RunTestCaseSet', testcaseset.RunTestCaseSet.as_view()),
]