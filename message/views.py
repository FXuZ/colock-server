from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm
from message.models import Message
from django.views.decorators.csrf import csrf_exempt

from colock.key_generator import *
from user_manage.authen import user_authen, hash2uid
from django.utils import timezone
import json
## send, upload, download


class SendForm(forms.Form):
    receiver_phone_hash = forms.CharField(max_length=32)
    sender_uid = forms.IntegerField()
    sender_ukey = forms.CharField(max_length=32)
    img = forms.FileField()


# this is not safe!!!
@csrf_exempt
def send(request):
    if request.method == "POST":
        send_form = SendForm(request.POST, request.FILES)
        if send_form.is_valid():
            sender_uid = send_form.cleaned_data['sender_uid']
            sender_ukey = send_form.cleaned_data['sender_ukey']

            if user_authen(sender_uid, sender_ukey):

                new_message = Message()
                img = request.FILES['img']

                new_message.sender_uid = sender_uid
                new_message.receiver_uid = hash2uid(send_form.cleaned_data['receiver_phone_hash'])
                new_message.send_time = timezone.now()
                new_message.message_key = message_key_gen(sender_uid, new_message.receiver_uid, new_message.send_time)
                new_message.img = img
                new_message.save()

                return_value = {'uid': new_message.id, 'ukey': new_message.message_key}
                return HttpResponse(json.dumps(return_value, ensure_ascii=False))
                # success and created new message
            else:
                return HttpResponse('Authen error')
        else:
            return render_to_response('register.html', {'uf': send_form, 'form': send_form})
    else:
        uf = SendForm()
        return render_to_response('register.html', {'uf':uf})
