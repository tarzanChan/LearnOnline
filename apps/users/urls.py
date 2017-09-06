# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import UserinfoView, UploadUserImageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),

    # 用户头像
    url(r'^image/upload/$', UploadUserImageView.as_view(), name='user_image_upload'),
]
