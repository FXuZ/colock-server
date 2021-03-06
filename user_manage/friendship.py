__author__ = 'Chengyu'
from user_manage.models import User
from user_manage.models import Friendship
from colock.Error import *
from colock import utils, settings
import os
from colock.key_generator import phone_hash_gen
import base64
import message.igt_wrappers as igt



@utils.hook()
def get_friend_list(meta, data, img):
    src_uid = meta['uid']
    query = Friendship.objects.filter(src_uid=src_uid)
    serial = [i.dest_uid for i in query]
    return '', {'status': 'done'}, {'query': serial}

# this is used when you switched to a new phone, we return all your friends



# adding friend needs to search first for the uid and information
# then use the information to add friend


@utils.hook()
def hash2uid(meta, data, img):
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
# def nickname2uid(meta, data, img):
#     # returns query list
#     input_nickname = data['nickname']
#     query = User.objects.filter(nickname=input_nickname)
#     if len(query) == 0:
#         raise UserNotExistError
#     return query


def is_friend_of(meta, data, img):
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


def can_send(sender_uid, receiver_uid):
    # only for server internal use
    # if not in blacklist, then you can send

    if sender_uid == receiver_uid:
        return True
    friendship = Friendship.objects.filter(src_uid=receiver_uid, dest_uid=sender_uid)
    if len(friendship) == 0:
        return False
    if friendship[0].friendship_type == 3:
        return False
    else:
        return True


@utils.hook()
def add_friend(meta, data, img):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship1 = Friendship.objects.filter(src_uid=dest_uid, dest_uid=src_uid)
    if len(friendship1) != 0:
        if friendship1[0].friendship_type == 0:
            raise BlockedfriendError

    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    dest = User.objects.get(id=dest_uid)
    src = User.objects.get(id=src_uid)
    if len(friendship) == 0:
        Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=1).save()
        dest = User.objects.get(id=dest_uid)

        # give the other person a notification
        igt.pushMsgToSingle_dispatch(receiver=dest, action='', meta={'status': 'Friend_Accepted'},
                                     data={'reg_num': src.region_num, 'phone_num': src.phone_num, 'uid':src.id})
        return '', {'status': 'done'}, {'reg_num': dest.region_num, 'phone_num': dest.phone_num}
    else:
        if friendship[0].friendship_type == 0:
            raise BlockfriendError
        if friendship[0].friendship_type != 1:
            raise FriendExistError
        # below is when type==1
        return '', {'status': 'done'}, {'reg_num': dest.region_num, 'phone_num': dest.phone_num}


@utils.hook()
def del_friend(meta, data, img):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    friendship[0].delete()
    return '', {'status': 'done'}, {}


@utils.hook()
def block_friend(meta, data, img):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=0)
        tmp_friend.save()
    else:
        friendship[0].friendship_type = 0
        friendship[0].save()

    return '', {'status': 'done'}, {}


@utils.hook()
def unblock_friend(meta, data, img):
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
def search_username(meta, data, img):
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


@utils.hook()
def update_user_info(meta, data, img):
    info_dict = data['info_dict']
    user = User.objects.get(id=int(meta['uid']))
    for (key, val) in info_dict.iteritems():
        if key != 'user_logo' and key != 'filetype':
            setattr(user, key, val)
    # if 'user_logo' in info_dict:
    #     User_Logo_Prefix = settings.BASE_DIR+'/upload/user_logo/'
    #     filename = User_Logo_Prefix + str(user.user_name) + info_dict['filetype']
    #     with open(filename, 'r+b') as f:
    #         f.write(info_dict['user_logo'].decode('base64'))
    #         user.user_logo(filename, f.read())

    if ('region_num' in info_dict) or ('phone_num' in info_dict):
        user.phone_hash = phone_hash_gen(user.region_num, user.phone_num)
    user.user_logo = img
    user.save()
    return '', {'status': 'done'}, {}


@utils.hook()
def blacklist_friend(meta, data, img):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
            tmp_friend = Friendship(src_uid=src_uid, dest_uid=dest_uid, friendship_type=3)
            tmp_friend.save()
    else:
        friendship[0].friendship_type = 3
        friendship[0].save()
    dest = User.objects.get(id=dest_uid)
    igt.pushMsgToSingle_dispatch(dest, '', meta={'status': 'Friend_Blacklisted'}, data={'uid': src_uid})
    return '', {'status': 'done'}, {}


@utils.hook()
def unblacklist_friend(meta, data, img):
    src_uid = meta['uid']
    dest_uid = data['dest_uid']
    friendship = Friendship.objects.filter(src_uid=src_uid, dest_uid=dest_uid)
    if len(friendship) == 0:
        raise FriendNotExistError
    if friendship[0].friendship_type != 0:
        raise NoNeedError
    friendship[0].friendship_type = 1
    # Action, Meta, Data
    dest = User.objects.get(id=dest_uid)
    igt.pushMsgToSingle_dispatch(dest, '', meta={'status': 'unBlacklist_friend'}, data={'uid': src_uid})
    return '', {'status': 'done'}, {}
