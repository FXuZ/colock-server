from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm
from user_manage.models import User
from django.views.decorators.csrf import csrf_exempt

from colock.key_generator import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['cid', 'phone_num', 'region_num', 'nickname']


# this is not safe!!!
@csrf_exempt
def register(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            new_user.ukey = user_key_gen()
            new_user.save()
            return HttpResponse(status=202)
            # success and created new user
    else:
        uf = RegisterForm()
    return render_to_response('register.html',{'uf':uf})