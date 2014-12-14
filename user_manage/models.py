from django.db import models
from django.utils import timezone


class User(models.Model):

    cid = models.CharField(max_length=32)
    ukey = models.CharField(max_length=32)
    # authentication key.

    region_num = models.IntegerField()
    phone_num = models.BigIntegerField()
    nickname = models.CharField(max_length=32)
    reg_time = models.DateTimeField(default=timezone.now)
    phone_hash = models.CharField(max_length=32)
    # no () means it's called every time instead of only when loading the model


class Friendship(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
    intimate = models.BooleanField()
    # uid1 is defined as the smaller one of the 2 id.
