import json
from user_manage.models import User
from colock import utils
__author__ = 'Chengyu'


@utils.hook('')
def is_valid_user(uid, ukey):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        return False, 'No such user id exists'
    elif query[0].ukey == ukey:
        return True, ''
    else:
        return False, 'Wrong key'

@utils.hook('')
def is_valid_uid(uid):
    query = User.objects.filter(id=uid)
    if len(query) == 0:
        return False, 'No such user id exists'
    else:
        return True, ''


@utils.hook('')
def is_valid_phone_num(reg_num,phone_num):
    return True, ''


@utils.hook('')
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
    if tmp_err[0]:

        # validate app_version and action

        # validate arguments needed for the action

        pass
    else:
        return tmp_err

