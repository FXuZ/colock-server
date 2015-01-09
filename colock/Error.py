__author__ = 'Chengyu'


class CustomError(Exception):
    pass


class UserError(CustomError):
    pass


class FriendshipError(CustomError):
    pass


class NoNeedError(CustomError):
    # This is for the case when your request have no need to be processed
    # e.g.: you are deleting a friendship that does not exist
    def __unicode__(self):
        return u"No need for this to be processed, the system is already in the state you want it to be"


class InvalidError(CustomError):
    # for bad raw inputs
    pass


class VersionError(CustomError):
    def __unicode__(self):
        return u"app version does not exist or no longer supported"


class AuthenError(CustomError):
    def __unicode__(self):
        return u"Unauthorized due to wrong ukey"

###############
# end of base class definition
###############


class UnknownActionError(VersionError):
    def __unicode__(self):
        return u"action does not exist or not supported in this version"


class InvalidNumberError(InvalidError):
    def __unicode__(self):
        return u"The input number value is not valid"


class InvalidJsonError(InvalidError):
    def __unicode__(self):
        return u"The input json value is not valid or cannot be parsed"


class InvalidMetaError(InvalidError):
    def __unicode__(self):
        return u"The input Request.Meta value is not valid or missing essential keys"


class InvalidDataError(InvalidError):
    def __unicode__(self):
        return u"The input Request.Data value is not valid or missing essential keys"


class UserNotExistError(UserError):
    def __unicode__(self):
        return u"No such user exists"


class WrongKeyError(UserError):
    def __unicode__(self):
        return u"Wrong ukey for this user id"


class BlockfriendError(FriendshipError):
    def __unicode__(self):
        return u"your friendship status with that user is blocked, please remove the user from your block list"


class BlockedfriendError(FriendshipError):
    def __unicode__(self):
        return u"request failed"
    # you are being blocked by someone so you see this


class FriendExistError(FriendshipError):
    def __unicode__(self):
        return u"you have already been friend with that user"


class FriendNotExistError(FriendshipError):
    def __unicode__(self):
        return u"your friend list does not include that user"