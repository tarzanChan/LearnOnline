# -*- coding: utf-8 -*-
__author__ = 'mengyuan'
__date__ = '2017/7/27 20:00'

import xadmin
from .models import Course, Lesson, Video, CourseResource

# list_display = []
# search_fields = []
# list_filter = []


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time',
                    'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['course_org__name', 'name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_nums']
    list_filter = ['course_org__name', 'name', 'desc', 'detail', 'degree', 'learn_time',
                   'students', 'fav_nums', 'image', 'click_nums', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
