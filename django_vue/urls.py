from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import api_test.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(api_test.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
