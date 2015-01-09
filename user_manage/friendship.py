__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship
from colock.Error import *
from colock import utils



def get_friend_list(meta, data):
    src_uid = meta['uid']
    query = Friendship.objects.filter(src_uid=src_uid)
    if len(query) == 0:
        raise UserNotExistError
    return query

# adding friend needs to search first for the uid and information
# then use the information to add friend


def hash2uid(input_hash_lst):
    # returns query list

    #######################
    query_lst = []
    for each in input_hash_lst:
        query_lst.append(User.objects.get(phone_hash=each))
    return query_lst
    ########################


def nickname2uid(meta, data):
    # returns query list
    input_nickname = data['nickname']
    query = User.objects.filter(nickname=input_nickname)
    if len(query) == 0:
        raise UserNotExistError
    return query


def is_friend_of(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    # return true if src can send a message to dest, also self is considered as friend
    if src_uid == dest_uid:
        return True
    friendship = Friendship.objects.filter(src_uid=dest_uid, dest_uid=src_uid)
    if len(friendship) == 0:
        return False
    else:
        if friendship[0].friendship_type == 0:
            return False
        else:
            return True


def add_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship1 = Friendship.objects.filter(src_uid=dest_uid, dest_uid=src_uid)
    if len(friendship1) != 0:
        if friendship1[0].friendship_type == 0:
            raise BlockedfriendError

    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=1).save()
    else:
        if friendship[0].friendship_type == 0:
            raise BlockfriendError
        if friendship[0].friendship_type != 1:
            raise FriendExistError


def del_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    if friendship[0].friendship_type == 0:
        raise NoNeedError
    friendship[0].friendship_type = -1


def block_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=0)
        tmp_friend.save()
    else:
        friendship[0].friendship_type = 0


def unblock_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    if friendship[0].friendship_type != 0:
        raise NoNeedError
    friendship[0].friendship_type = 1


