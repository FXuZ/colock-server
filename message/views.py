from django.shortcuts import render
# import django.http
from django.http import HttpResponse
from django.forms import ModelForm
from message.models import Message
from message.models import upload_prefix
from django.views.decorators.csrf import csrf_exempt
from sendfile import sendfile

class DownloadForm(ModelForm):
    class Meta:
        fields = ['message_key']

# Create your views here.
# def send(request):

@csrf_exempt
def download(request):
    if request.method == "POST":
        msg_id = int( request.POST["message_id"] )
        msg_key = request.POST["message_key"]
        if Message.objects.get(id=msg_id).message_key == msg_key:
            filepath = ( "%s/%s" % ( upload_prefix, msg_key ) )
            img_file = open(filepath)
            # make a response
            return sendfile(img_file)
    else:
        return HttpResponse(status=405)
    # print request.POST
