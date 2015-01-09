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


def is_valid_dispatch(action, meta, data):
    # return (boolean, string), string is the error information, and if it's valid string will be blank
    try:
        dict_meta = json.loads(meta)
        dict_data = json.loads(data)
    except:
        raise InvalidJsonError
    try:
        sender_uid = dict_meta['sender_uid']
        sender_ukey = dict_meta['sender_uid']
        app_version = dict_meta['app_version']
    except:
        raise InvalidMetaError

    tmp_err = is_valid_user(sender_uid, sender_ukey)
    if not tmp_err[0]:
        return tmp_err
    disp_lst = json.load(BASE_DIR + 'dispatch-list.json')

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
        return True

