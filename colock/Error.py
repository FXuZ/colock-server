__author__ = 'Chengyu'


class BlockfriendError(Exception):
    def __unicode__(self):
        return u"your friendship status with that user is blocked, please remove the user from your blocklist"


class BlockedfriendError(Exception):
    def __unicode__(self):
        return u"request failed"
    # you are being blocked by someone so you see this


class FriendExistError(Exception):
    def __unicode__(self):
        return u"you have already been friend with that user"
