# -*- coding:utf-8 -*-
__author__ = 'Chengyu'
import hashlib


def user_key_gen(uid, region_num, phone_num, datetime):
    key = str(uid) + str(region_num) + str(phone_num) + str(datetime)
    key = hashlib.new("md5", key).hexdigest()
    return key


def message_key_gen(sender_uid, receiver_uid, datetime):
    key = str(sender_uid) + str(receiver_uid) + str(datetime)
    key = hashlib.new("md5", key).hexdigest()
    return key


def phone_hash_gen(region_num,phone_num):
    salt = "Christina"
    key = str(region_num) + salt + str(phone_num)
    key = hashlib.new("md5", key).hexdigest()
    return key