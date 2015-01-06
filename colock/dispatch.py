#!/bin/env python2
# -*- encoding:utf-8 -*-

from django.shortcuts import render_to_response
from django import forms
import colock.settings
from importlib import import_module
from colock import utils
from django.views.decorators.csrf import csrf_exempt

imported_modules = []
class dispatchForm(forms.Form):
    Action = forms.CharField(max_length=32)
    Meta = forms.CharField()
    Data = forms.CharField()

for mod in colock.settings.DISPATCH_MANAGED_APPS:
    imported_modules.append(import_module(mod + ".views"))

@csrf_exempt
def dispatch(request):
    if request.method == "POST":
        action = request.POST["Action"]
        return utils.call_hook(action, request.POST["Meta"], request.POST["Data"])
    else:
        return render_to_response('register.html',
                    {'uf': dispatchForm()})

