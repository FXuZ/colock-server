import json
from user_manage.models import User
from colock import utils
import os
from settings import BASE_DIR
from Error import *
__author__ = 'Chengyu'


@utils.hook()
def is_valid_user(uid, ukey):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        raise UserNotExistError
    elif query[0].ukey == ukey:
        return True
    else:
        raise AuthenError


@utils.hook()
def is_valid_uid(uid):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        raise UserNotExistError
    return True


@utils.hook()
def is_valid_reg_num(reg_num):
    allowed_lst = (1, 86)
    if reg_num not in allowed_lst:
        raise InvalidError
    else:
        return True


@utils.hook()
def is_valid_phone_num(phone_num):
    return True


@utils.hook()
def is_valid_user_info_dict(info_dict):
    # ALLOWED_KEY = {'cid': ['is_valid_cid'], 'region_num': ['is_valid_reg_num'], 'phone_num': ['is_valid_phone_num'],
    #                'nick_name': ['is_valid_user_name'], 'user_logo': ['is_valid_user_logo'], 'filetype': ['is_valid_filetype']}
    #
    # for (key, val) in info_dict.iteritems:
    #     if key not in ALLOWED_KEY:
    #         raise InvalidError
    #         # not allowed keys

    #
    return True


def is_valid_dispatch(action, meta, data):
    # return (boolean, string), string is the error information, and if it's valid string will be blank
    try:
        dict_meta = json.loads(meta)
        dict_data = json.loads(data)
    except:
        raise InvalidJsonError
    try:
        sender_uid = dict_meta['uid']
        sender_ukey = dict_meta['ukey']
        app_version = dict_meta['app_version']
    except:
        raise InvalidMetaError

    try:
        tmp = is_valid_user(sender_uid, sender_ukey)
    except AuthenError:
        raise AuthenError
    with open(BASE_DIR + '/dispatch-list.json') as f:
        disp_lst = json.load(f)

    # validate app_version and action
    if app_version not in disp_lst:
        raise VersionError

    v_lst = disp_lst[app_version]
    if action not in v_lst:
        raise UnknownActionError

    # validate arguments needed for the action
    arg_lst = v_lst[action]
    for i in arg_lst:
        if i not in dict_data:
            raise InvalidDataError
        for j_validation in arg_lst[i]:
            try:
                utils.call_hook(j_validation, dict_data[i])
            except (VersionError, InvalidError) as err:
                raise err
    else:
        return action, dict_meta, dict_data

#Add to a form containing a FileField and change the field names accordingly.
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.forms import forms


def clean_content(self):
    content = self.cleaned_data['content']
    content_type = content.content_type.split('/')[0]
    if content_type in settings.CONTENT_TYPES:
        if content._size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
    else:
        raise forms.ValidationError(_('File type is not supported'))
    return content