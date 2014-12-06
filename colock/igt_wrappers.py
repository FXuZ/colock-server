#!/bin/env python2
# -*- coding: utf-8 -*-

# 个推api wrapper

from igt_push import IGeTui
from igetui.template.igt_transmission_template import TransmissionTemplate
from igetui.igt_message import IGtSingleMessage
from igetui.igt_target import Target
import json
import hashlib

APPKEY = "JqIuzNCh8xA8wXduUKM9E"
APPID = "7mgfcIRMfD9WYxM9OqFao4"
MASTERSECRET = "3zML5QG36Z5MfH3iXQX004"
APPSECRET = "O7iYcIua0tAipzGlMOtW67"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'
PRIV_HOST = 'http://rumisato.fxyk.tk/download/'

def pushImageToSingle(sender, receiver, message):
    '''
    push message uploaded from sender to receiver
    sender and receiver are User objects,
    message is string
    '''
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    trasmission_data = TransmissionTemplate()
    trasmission_data.transmissionType = 1
    trasmission_data.appId = APPID
    trasmission_data.appKey = APPKEY
    trasmission_data.transmissionContent = makeMessage(sender, receiver, message)
    trasmission_data.setPushInfo("", 2, "", "", "", "", "", 1)

    igt_message = IGtSingleMessage()
    igt_message.isOffline = True
    igt_message.offlineExpireTime = 1000 * 3600 * 12
    igt_message.data = trasmission_data
    igt_message.pushNetWorkType = 2

    igt_target = Target()
    igt_target.appId = APPID
    igt_target.clientId = receiver.cid

    ret = push.pushMessageToSingle(igt_message, igt_target)
    return ret


def makeMessage(sender, receiver, message):
    msg_body = {
        "sender_region": sender.region_num,
        "sender_phone": hashlib.md5(sender.phone_num).digest(),
        "message_key": message.message_key,
        "send_time": message.send_time,
    }
    return json.dump(msg_body)


