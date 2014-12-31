__author__ = 'Chengyu'


class BlockfriendError(Exception):
    def __unicode__(self):
        return "your friendship status with that user is blocked, please remove the user from your blocklist"


class BlockedfriendError(Exception):
    def __unicode__(self):
        return "request failed"
    # you are being blocked by someone so you see this


class FriendExistError(Exception):
    def __unicode__(self):
        return "you have already been friend with that user"
