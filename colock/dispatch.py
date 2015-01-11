#!/bin/env python2
# -*- encoding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
import colock.settings
from importlib import import_module
from colock.utils import call_hook

from colock import utils, validation
from django.views.decorators.csrf import csrf_exempt
import json

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
        meta = request.POST["Meta"]
        data = request.POST["Data"]
        is_valid, error_msg = validation.is_valid_dispatch(action, meta, data)
        if is_valid:
            response_action, response_meta, response_data = utils.call_hook(action, meta, data)
            response = HttpResponse()
            response_dict = {"Action": response_action,
                             "Meta": response_meta,
                             "Data": response_data}
            response.write(json.dumps(response_dict))
            return response
        else:
            return HttpResponse(error_msg, status=500)
    else:
        return render_to_response('register.html',
                    {'uf': dispatchForm()})

