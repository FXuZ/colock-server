from django.db import models
from django.utils import timezone


class User(models.Model):

    cid = models.IntegerField()
    ukey = models.CharField(max_length=32)
    # authentication key.

    region_num = models.IntegerField()
    phone_num = models.BigIntegerField()
    nickname = models.CharField(max_length=32)
    reg_time = models.DateTimeField(default=timezone.now)
    # no () means it's called every time instead of only when loading the model



