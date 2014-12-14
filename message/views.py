from django.shortcuts import render, render_to_response
from django import forms
# import django.http
from django.http import HttpResponse
from message.models import Message
from message.models import upload_prefix
from django.views.decorators.csrf import csrf_exempt

from colock.key_generator import *
from user_manage.authen import user_authen, hash2uid
from django.utils import timezone
import json

from igt_wrappers import pushMsgToSingle

class SendForm(forms.Form):
    receiver_uid = forms.IntegerField()
    sender_uid = forms.IntegerField()
    sender_ukey = forms.CharField(max_length=32)
    filetype = forms.CharField(max_length=10)
    img = forms.FileField()


class DownloadForm(forms.Form):
    message_id = forms.IntegerField()
    message_key = forms.CharField(max_length=32)

# Create your views here.


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
                new_message.receiver_uid = send_form.cleaned_data['receiver_uid']
                new_message.send_time = timezone.now()
                new_message.message_key = message_key_gen(sender_uid, new_message.receiver_uid, new_message.send_time)
                new_message.img = img
                new_message.filetype = send_form.cleaned_data['filetype']
                new_message.save()

                return_value = {'message_id': new_message.id, 'message_key': new_message.message_key}
#                 sender = User.objects.get(int(sender_uid))
#                 receiver = User.objects.get(int(send_form.cleaned_data['receiver_uid']))
#                 igt_ret = pushMsgToSingle(sender, receiver, new_message)
#                 if DEBUG == True:
#                     print igt_ret
                return HttpResponse(json.dumps(return_value, ensure_ascii=False))
                # success and created new message
            else:
                return HttpResponse('Authen error')
        else:
            return render_to_response('register.html', {'uf': send_form, 'form': send_form})
    else:
        uf = SendForm()
        return render_to_response('register.html', {'uf':uf})

@csrf_exempt
def download(request):
    if request.method == "POST":
        msg_id = int( request.POST["message_id"] )
        msg_key = request.POST["message_key"]
        msg = Message.objects.get(id=msg_id)
        if msg.message_key == msg_key:
            msg.exist = False
            msg.save()
            filepath = ( "%s/%s" % ( upload_prefix, msg_key ) )
            img_file = open(filepath)
            # make a response
            res = HttpResponse( img_file, content_type = 'image/%s' % msg.filetype )
            res['Content-Disposition'] = 'attachment; filename=%s.%s' % (msg_key, msg.filetype)
            return res
        else:
            return HttpResponse("Message not exist",status=404);
    else:
        return render_to_response('register.html', {'uf': DownloadForm()})
    # print request.POST

