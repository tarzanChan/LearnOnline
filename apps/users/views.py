# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class ActiveUserView(View):
    """
    用户邮箱激活验证,注意此处只有get方法，如果有post方法，前端{% url 'xxx' %}
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
        else:
            return render(request, "active_fail.html", {})

        return render(request, "index.html", {})


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")

            # 判断用户邮箱是否已被注册
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {'register_form': register_form, 'msg': "用户已经存在"})

            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, "index.html", {})
        else:
            return render(request, "register.html", {'register_form': register_form})


class LoginView(View):
    """
    用类的方法完成登录功能
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)    # 此处传入一个字典

        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {'msg': '用户名未激活'})
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误'})
        else:
            return render(request, "login.html", {"login_form": login_form})


# Create your views here.
class CustomBackend(ModelBackend):
    """
    当我们想要扩展校验条件时，可以重载authenticate方法，该方法需要：
        1）from django.contrib.auth.backends import ModelBackend

        2）在setting中加入：
        AUTHENTICATION_BACKENDS = (
        'users.views.CustomBackend',  #加入支持的类

        )
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # user = UserProfile.objects.get(username=username)
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用方法的方式来完成登录功能
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {'msg': '用户名或密码错误'})
#     elif request.method == "GET":
#         return render(request, "login.html", {})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetPasswordView(View):
    """
    重置密码
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html", {})
        return render(request, "index.html", {})


class ModifyPasswordView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 != password2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})

