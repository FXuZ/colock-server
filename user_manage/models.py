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
    phone_hash = models.CharField(max_length=32, db_index=True)
    # no () means it's called every time instead of only when loading the model

    def __unicode__(self):
        return unicode(self.id)


class Friendship(models.Model):
    # directed
    src_uid = models.IntegerField()
    dest_uid = models.IntegerField()
    friendship_type = models.IntegerField()
    # type0: src blocked dest, type1: src has phone num of dest, type2: src view dest as intimate

