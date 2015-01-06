__author__ = 'Chengyu'
from user_manage.models import User
import json


def user_authen(uid, ukey):
    user = User.objects.get(id=uid)
    if user.ukey == ukey:
        return True
    else:
        return False


