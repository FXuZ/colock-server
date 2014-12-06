from django.shortcuts import render, render_to_response
from django import forms
# import django.http
from django.http import HttpResponse
from django.forms import ModelForm
from message.models import Message
from message.models import upload_prefix
from django.views.decorators.csrf import csrf_exempt
from sendfile import sendfile


from colock.key_generator import *
from user_manage.authen import user_authen, hash2uid
from django.utils import timezone
import json

class SendForm(forms.Form):
    receiver_phone_hash = forms.CharField(max_length=32)
    sender_uid = forms.IntegerField()
    sender_ukey = forms.CharField(max_length=32)
    img = forms.FileField()

class DownloadForm(ModelForm):
    message_id = forms.IntegerField()
    message_ukey = forms.CharField(max_length=32)

# Create your views here.

# this is not safe!!!
@csrf_exempt
def send(request):
    if request.method == "POST":
        send_form = SendForm(request.POST)
        if send_form.is_valid():
            sender_uid = send_form.cleaned_data['sender_uid']
            sender_ukey = send_form.cleaned_data['sender_ukey']

            if user_authen(sender_uid, sender_ukey):
                new_message = Message()
                img = send_form.img
                new_message.sender_uid = sender_uid
                new_message.receiver_uid = hash2uid(send_form.cleaned_data['receiver_phone_hash'])
                new_message.sendtime = timezone.now()
                new_message.message_key = message_key_gen(sender_uid, new_message.receiver_uid, new_message.sendtime)
                new_message.img = img
                new_message.save()

                return_value = {'uid': new_message.id, 'ukey': new_message.ukey}
                return HttpResponse(json.dumps(return_value, ensure_ascii=False))
                # success and created new message
            else:
                return HttpResponse(status=403)
    else:
        uf = SendForm()
    return render_to_response('register.html',{'uf':uf})

@csrf_exempt
def download(request):
    if request.method == "POST":
        msg_id = int( request.POST["message_id"] )
        msg_key = request.POST["message_key"]
        if Message.objects.get(id=msg_id).message_key == msg_key:
            msg = Message.objects.get(id=msg_id)
            msg.exist = False
            msg.save()
            filepath = ( "%s/%s" % ( upload_prefix, msg_key ) )
            img_file = open(filepath)
            # make a response
            # from django-sendfile
            return sendfile(img_file)
        else:
            return HttpResponse(status=404,"Message not exist");
    else:
        return HttpResponse(status=405)
    # print request.POST
