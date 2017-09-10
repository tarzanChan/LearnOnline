# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import UserinfoView, UploadUserImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

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

    # 我的学习课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 我的收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 我的收藏课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 我的收藏讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

]
