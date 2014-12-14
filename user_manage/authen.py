__author__ = 'Chengyu'
from user_manage.models import User


def user_authen(uid, ukey):
    user = User.objects.get(id=uid)
    if user.ukey == ukey:
        return True
    else:
        return False


def hash2uid(hash):
    uid = 1
    return uid