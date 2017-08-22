# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from django.http import HttpResponse
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        # 城市
        all_cities = CityDict.objects.all()

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


        #取出热门课程排序
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

            #此处需要返回JSON，做异步操作
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg': {0}}".format(userAskForm.errors), content_type='application/json')