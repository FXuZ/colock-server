__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship


def get_friend_list(src_uid):
    return "bidiu!"


def is_friend():
    # blacklist is not friend!

    return True


# adding friend needs to search first for the uid and information
# then use the information to add friend


def hash2uid(input_hash):
    # returns query list
    user = User.objects.filter(phone_hash=input_hash)
    return user


def nickname2uid(input_nickname):
    # returns query list
    user = User.objects.filter(nickname=input_nickname)
    return user


def add_friend(src_uid, dest_uid):

    # first check no friendship or blacklist existed between them
    pass

    # if one side is blocked





def block_friend(src_uid, dest_uid):
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=0)
        tmp_friend.save()
    else:
        friendship[0].friendship_type = 0







