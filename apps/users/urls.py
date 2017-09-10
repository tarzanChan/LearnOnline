# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import UserinfoView, UploadUserImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),

    # 用户头像
    url(r'^image/upload/$', UploadUserImageView.as_view(), name='user_image_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='user_update_pwd'),

    # 发送邮箱验证码
    url(r'^send_email_code/$', SendEmailCodeView.as_view(), name='send_email_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='upadate_email'),

]
