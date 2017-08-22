# -*- coding: utf-8 -*-
__author__ = 'mengyuan'
__date__ = '2017/8/22 20:35'

from django import forms
from operation.models import UserAsk

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']