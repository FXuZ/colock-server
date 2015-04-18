__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship
from colock.Error import *
from colock import utils, settings
import os


@utils.hook()
def get_friend_list(meta, data):
    src_uid = meta['uid']
    query = Friendship.objects.filter(src_uid=src_uid)
    serial = [i.dest_uid for i in query]
    return '', {'status': 'done'}, {'query': serial}

# this is used when you switched to a new phone, we return all your friends



# adding friend needs to search first for the uid and information
# then use the information to add friend


@utils.hook()
def hash2uid(meta, data):
    # returns query list
    ret = []
    for hash_ite in data['phone_hash_list']:
        qry = User.objects.filter(phone_hash=hash_ite)
        for ii in range(len(qry)):
            try:
                ####################
                # low efficiency
                ####################
                add_friend(meta, {'dest_uid': qry[ii].id})
                ret.append(unicode(hash_ite))
                ret.append(qry[ii].id)
        #############
            except FriendshipError:
                pass
    return '', {'status': 'done'}, {'query': ret}


# @utils.hook()
# def nickname2uid(meta, data):
#     # returns query list
#     input_nickname = data['nickname']
#     query = User.objects.filter(nickname=input_nickname)
#     if len(query) == 0:
#         raise UserNotExistError
#     return query


def is_friend_of(meta, data):
    # only for server internal use
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    # return true if src can send a message to dest, also self is considered as friend
    if src_uid == dest_uid:
        return True
    friendship = Friendship.objects.filter(src_uid=dest_uid, dest_uid=src_uid)
    if len(friendship) == 0:
        return False
    else:
        if friendship[0].friendship_type <= 0:
            return False
        else:
            return True


@utils.hook()
def add_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship1 = Friendship.objects.filter(src_uid=dest_uid, dest_uid=src_uid)
    if len(friendship1) != 0:
        if friendship1[0].friendship_type == 0:
            raise BlockedfriendError

    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    dest = User.objects.get(id=dest_uid)
    if len(friendship) == 0:
        Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=1).save()
        dest = User.objects.get(id=dest_uid)
        return '', {'status': 'done'}, {'reg_num': dest.region_num, 'phone_num': dest.phone_num}
    else:
        if friendship[0].friendship_type == 0:
            raise BlockfriendError
        if friendship[0].friendship_type != 1:
            raise FriendExistError
        # below is when type==1
        return '', {'status': 'done'}, {'reg_num': dest.region_num, 'phone_num': dest.phone_num}


@utils.hook()
def del_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    if friendship[0].friendship_type == 0:
        raise BlockfriendError
    friendship[0].friendship_type = -1
    return '', {'status': 'done'}, {}


@utils.hook()
def block_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=0)
        tmp_friend.save()
    else:
        friendship[0].friendship_type = 0
    return '', {'status': 'done'}, {}


@utils.hook()
def unblock_friend(meta, data):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    if friendship[0].friendship_type != 0:
        raise NoNeedError
    friendship[0].friendship_type = 1
    # Action, Meta, Data
    return '', {'status': 'done'}, {}


@utils.hook()
def search_username(meta, data):
    src_uid = meta['uid']
    username = str(data['username'])
    query = User.objects.filter(user_name=username)
    query2 = User.objects.filter(user_name=username, user_logo__isnull=True)
    if len(query) == 0:
        raise FriendNotExistError
    data = {'id': query[0].id, 'nickname': query[0].nickname}


    ###
    User_Logo_Prefix = settings.BASE_DIR+'/upload/'
    ###

    if len(query2) != len(query):
        try:
            path = query[0].user_logo.url
            path = User_Logo_Prefix + path
            fn, ext = os.path.splitext(path)
            f = open(path)
            content = f.read().encode("base64")
            data['user_logo'] =  content
            data['filetype'] = ext
            f.close()
        except:
            pass

    return '', {'status': 'done'}, data


