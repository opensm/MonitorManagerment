"""OpsCMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from Collect import views

urlpatterns = [
    # 加载上传资源
    # 使用re_path 支持正则表达式
    re_path('^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('admin/', admin.site.urls),
    path('rbac/', include('rbac.urls')),
    path('monitor/', include('monitor.urls')),
    path('index/', views.IndexView.as_view(), name='index')
]
