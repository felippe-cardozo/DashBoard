"""tasks URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from dashboard import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.dashboard, name='dashboard'),
    url("^soc/", include("social_django.urls", namespace="social")),
    url(r'^update/(?P<task_id>[0-9]+)/$', views.update, name='update'),
    url(r'^new/', views.new, name='new'),
    url(r'^destroy/(?P<task_id>[0-9]+)/$', views.destroy, name='destroy'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^done/(?P<task_id>[0-9]+)/$', views.mark_as_done, name='done'),
    url(r'^logout/', views.log_out, name='log_out')
]
