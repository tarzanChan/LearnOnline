# -*- coding: utf-8 -*-
from .views import OrgView, AddUserAskView
from django.conf.urls import url, include


urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask$', AddUserAskView.as_view(), name="add_ask")
]