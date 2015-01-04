__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship
from colock.Error import *

def get_friend_list(src_uid):
    return Friendship.objects.filter(src_uid=src_uid)


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

    friendship1 = Friendship.objects.filter(dest_uid,src_uid)
    if len(friendship1) != 0:
        if friendship1[0].friendship_type == 0:
            raise BlockedfriendError

    friendship = Friendship.objects.filter(src_uid, dest_uid)
    if len(friendship) == 0:
        Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=1).save()
    else:
        if friendship[0].friendship_type == 0:
            raise BlockfriendError
        if friendship[0].friendship_type != 1:
            raise FriendExistError


def block_friend(src_uid, dest_uid):
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=0)
        tmp_friend.save()
    else:
        friendship[0].friendship_type = 0







