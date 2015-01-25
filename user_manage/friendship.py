__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship
from colock.Error import *
from colock import utils


@utils.hook()
def get_friend_list(meta, data):
    src_uid = meta['uid']
    query = Friendship.objects.filter(src_uid=src_uid)
    if len(query) == 0:
        raise UserNotExistError
    return query

# adding friend needs to search first for the uid and information
# then use the information to add friend


@utils.hook()
def hash2uid(meta, data):
    # returns query list

    for hash_ite in data['phone_hash']:
        qry = User.objects.filter(phone_hash=hash_ite)
        ret = []
        if len(qry) != 0:
            try:
                ####################
                # low efficiency
                ####################
                add_friend(meta=meta, data={'dest_uid': qry[0].id})
                ret.append([qry[0].id, hash_ite])
        #############
            except FriendshipError:
                pass
        return ret


@utils.hook()
def nickname2uid(meta, data):
    # returns query list
    input_nickname = data['nickname']
    query = User.objects.filter(nickname=input_nickname)
    if len(query) == 0:
        raise UserNotExistError
    return query


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

