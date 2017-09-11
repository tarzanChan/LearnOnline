# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
import json


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 城市
        all_cities = CityDict.objects.all()

        # 机构全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        # (这里因为city属于CourseOrg的一个外键，在数据库中存储的是city_id,
        # 所以这里filter_city得到的是一个字符串类型的id,而不是一个city类实例)
        filter_city = request.GET.get('city', "")
        if filter_city:
            all_orgs = all_orgs.filter(city_id=int(filter_city))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 机构总数
        org_nums = all_orgs.count()

        # 取出热门课程排序
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        # 第二个参数代表每一页显示的个数
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "filter_city": filter_city,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userAskForm = UserAskForm(request.POST)
        if userAskForm.is_valid():
            # 注意form 和 Modelform 的区别
            # 这里使用Modelform的save方法获取一个Model实例，并且使commit为True表示结束后会把实例保存到数据库
            user = userAskForm.save(commit=True)
            suc_dict = {'status': 'success'}
            return HttpResponse(json.dumps(suc_dict), content_type="application/json")
            # return HttpResponse("{'status': 'success'}", content_type="application/json")
        else:
            error_dict = {'status': 'fail', 'msg': u'填写错误'}
            return HttpResponse(json.dumps(error_dict), content_type="application/json")
            # return HttpResponse("{'status': 'fail', 'msg': u'填写错误'}", content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        # 这里course_org的course_set方法用来获取反向内容，因为CourseOrg是Course的一个外键，所以可以通过该方法反向获取出所有的Course
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        # 这里course_org的course_set方法用来获取反向内容，因为CourseOrg是Course的一个外键，所以可以通过该方法反向获取出所有的Course
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        # 这里course_org的course_set方法用来获取反向内容，因为CourseOrg是Course的一个外键，所以可以通过该方法反向获取出所有的Course
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        # 这里course_org的course_set方法用来获取反向内容，因为CourseOrg是Course的一个外键，所以可以通过该方法反向获取出所有的Course
        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            "all_teachers": all_teachers,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        fail_collect = {'status': 'fail', 'msg': u'用户未登录'}
        success_collect = {'status': 'success', 'msg': u'已收藏'}
        not_collect = {'status': 'success', 'msg': u'收藏'}
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse(json.dumps(fail_collect), content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在表示用户取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse(json.dumps(not_collect), content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse(json.dumps(success_collect), content_type="application/json")
            else:
                return HttpResponse(json.dumps(fail_collect), content_type="application/json")


class TeacherListView(View):
    def get(self, request):

        all_teachers = Teacher.objects.all()

        # 教师全局搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        # 对教师进行排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sort_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        # 第二个参数代表每一页显示的个数
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            "all_teachers": teachers,
            "sort_teachers": sort_teachers,
            "sort": sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        teacher_teach_courses = Course.objects.filter(teacher=teacher)

        sort_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            "teacher_teach_courses": teacher_teach_courses,
            "sort_teachers": sort_teachers,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved": has_org_faved,
        })
