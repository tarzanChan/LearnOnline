# _*_ encoding:utf-8 _*_
from django.shortcuts import render

# Create your views here.
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import CourseOrg, CityDict

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_cities = CityDict.objects.all()

        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        objects = ['john', 'edward', 'josh', 'frank']

        # Provide Paginator with the request object for complete querystring generation
        # 第二个参数代表每一页显示的个数
        p = Paginator(all_orgs, 2, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
        })
