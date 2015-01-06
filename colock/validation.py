import json
from user_manage.models import User
from colock import utils
import os
from settings import BASE_DIR
__author__ = 'Chengyu'


@utils.hook()
def is_valid_user(uid, ukey):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        return False, 'No such user id exists'
    elif query[0].ukey == ukey:
        return True, ''
    else:
        return False, 'Wrong key'


@utils.hook()
def is_valid_uid(uid):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        return False, 'No such user id exists'
    else:
        return True, ''


@utils.hook()
def is_valid_phone_num(reg_num,phone_num):
    return True, ''


@utils.hook()
def is_valid_dispatch(action, meta, data):
    # return (boolean, string), string is the error information, and if it's valid string will be blank
    try:
        dict_meta = json.loads(meta)
        dict_data = json.loads(data)
    except:
        return False, 'meta or data cannot be parsed as json'
    try:
        sender_uid = dict_meta['sender_uid']
        sender_ukey = dict_meta['sender_uid']
        app_version = dict_meta['app_version']
    except:
        return False, 'essential information missing in meta'

    tmp_err = is_valid_user(sender_uid, sender_ukey)
    if not tmp_err[0]:
        return tmp_err
    disp_lst = json.load(BASE_DIR + 'dispatch-list.json')

    # validate app_version and action
    if app_version not in disp_lst:
        return False, 'app version does not exist or no longer supported'

    v_lst = disp_lst[app_version]
    if action not in v_lst:
        return False, 'action does not exist or not supported in this version'

    # validate arguments needed for the action
    arg_lst = v_lst[action]
    for i in arg_lst:
        if i not in dict_data:
            return False, 'Missing argument %s for action %s' % (action, i)
        for j_validation in arg_lst[i]:
            bingo, reason = utils.call_hook(j_validation, dict_data[i])
            if not bingo:
                return bingo, reason
            else:
                return True, ''

