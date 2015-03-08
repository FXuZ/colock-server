from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm
from user_manage.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from colock.key_generator import *
import json


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['cid', 'phone_num', 'region_num', 'nickname', 'user_name', 'user_logo']


class RegisterReturnForm(forms.Form):
    uid = forms.IntegerField()
    ukey = forms.CharField(max_length=32)


# this is not safe!!!
@csrf_exempt
def register(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            new_user = reg_form.save(commit=False)
            new_user.reg_time = timezone.now()
            new_user.ukey = user_key_gen(new_user.id, new_user.region_num, new_user.phone_num, new_user.reg_time)
            new_user.phone_hash = phone_hash_gen(new_user.region_num, new_user.phone_num)
            new_user.save()

            return_value = {'uid': new_user.id, 'ukey': new_user.ukey}
            # ensure_ascii=False to handle Chinese
            return HttpResponse(json.dumps(return_value, ensure_ascii=False))
            # success and created new user
    else:
        uf = RegisterForm()
    return render_to_response('register.html', {'uf': uf})
