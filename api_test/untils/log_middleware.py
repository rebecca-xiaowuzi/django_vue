from django.utils.deprecation import MiddlewareMixin
import time
import json
import urllib.parse
from rest_framework.parsers import JSONParser
# 获取日志logger
import logging

logger = logging.getLogger(__name__)

#日志中间件
class LogMiddle(MiddlewareMixin):

    def __init__(self, *args):
        super(LogMiddle, self).__init__(*args)

        self.start_time = None  # 开始时间
        self.end_time = None  # 响应时间
        self.data = {}  # dict数据

    # 日志处理中间件
    def process_request(self, request):
        # 存放请求过来时的时间
        self.start_time = time.time()  # 开始时间
        re_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 请求时间（北京）
        # 请求IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # 如果有代理，获取真实IP
            re_ip = x_forwarded_for.split(",")[0]
        else:
            re_ip = request.META.get('REMOTE_ADDR')
        # 请求方法
        re_method = request.method
        #存放请求
        if re_method=='GET':
            re_content = json.dumps(request.GET)
        else:
            re_content = request.body
        self.data.update(
            {
                're_time': re_time,  # 请求时间
                're_url': request.path,  # 请求url
                're_method': re_method,  # 请求方法
                're_ip': re_ip,  # 请求IP
                're_content': re_content  # 请求参数
                # 're_user': 'AnonymousUser'  # 匿名操作用户测试
            }
        )

    def process_response(self, request, response):
        try:

            # 请求url在 exclude_urls中，直接return，不保存操作日志记录
            # for url in self.__exclude_urls:
            #     if url in self.data.get('re_url'):
            #         return response
            # 获取响应数据字符串(多用于API, 返回JSON字符串)
            rp_content = str(response.content.decode('utf-8'))
            rp_content = urllib.parse.unquote(rp_content)
            rp_content = (json.loads(rp_content))
            self.data['rp_content'] = rp_content
            # 耗时
            self.end_time = time.time()  # 响应时间
            access_time = self.end_time - self.start_time
            self.data['access_time'] = round(access_time * 1000)  # 耗时毫秒/ms
            logger.info(self.data)
        except:
            logger.critical('系统错误')
        return response