#!/bin/env python2
# -*- encoding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
import json
import colock.settings
from importlib import import_module
from colock.utils import call_hook


def dispatch(request):
    if request.method == "POST":
        body = json.loads(request.POST["body"])
        return call_hook(body["Action"], request)
    else:
        form_content = {
            'Action': '',
            'Meta': '',
            'Data': ''
        }
        return render_to_response('register.html',
                    {'uf': forms.Form(form_content)})

