from datetime import datetime, timezone
from django.conf import settings
from core.constants import identifer as idf

utc_dt = datetime.now(timezone.utc)

class BaseException(Exception):
    err_resp = {}
    err_resp[idf.ERR] = {}

    err_resp[idf.ERR][idf.ERR_TIMESTMP] = utc_dt.astimezone().isoformat()
    err_resp[idf.ERR][idf.ERR_VERSION] = settings.APP_VERSION
    err_resp[idf.ERR][idf.ERR_CODE] = "00"
    err_resp[idf.ERR][idf.ERR_MSG_ID] = ""
    err_resp[idf.ERR][idf.ERR_MSG] = ""
    err_resp[idf.ERR][idf.ERR_DETAIL] = ""
    err_resp[idf.ERR][idf.ERR_PATH] = ""
    err_resp[idf.ERR][idf.STATUS_CODE] = 404

    def __init__(self):
        self.err_resp = self.err_resp

class DefaultError(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "15"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_DEFAULT"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Server encountered a problem."
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please check logs for details"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)


class HTTP401Error(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "1"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_UNAUTHORIZED"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Invalid Username/Password."
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please try again"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 401

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)

class HTTP404Error(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "06"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_NOT_FOUND"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Resource cannot be found"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "The requested resource does not exist"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 404

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)

class TokenInvalidError(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "07"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_TOKEN"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Token is invalid"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "The token has expired/invalid"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 403

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)

class HTTP403Error(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "9"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_PERMISSION"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "User has no permission"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "User has no permission"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 403

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)


class RoomDeleteError(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_ROOM_DELETE"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Unable to delete room"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please transfer the devices to other room"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 409

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)


class DeviceNotFoundError(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_DEVICE_NOT_FOUND"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Device not found"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please try again"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)


class UserNotFoundError(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_USER_NOT_FOUND"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "User is invalid or does not exist"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please try again"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)
        
class UsernameAlreadyExist(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_USERNAME_ALREADY_EXIST"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Username already exist"
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please try again"
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)

class DeviceAlreadyAssigned(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_DEVICE_ALREADY_ASSIGNED"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Device Key already assigned to other home."
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please add other device."
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)
class DeviceAlreadyAdded(BaseException):
    def __init__(self, *args, **kwargs):
        self.err_resp[idf.ERR][idf.ERR_CODE] = "10"
        self.err_resp[idf.ERR][idf.ERR_MSG_ID] = "ERR_DEVICE_ALREADY_ASSIGNED"
        self.err_resp[idf.ERR][idf.ERR_MSG] = "Device Key already assigned to this home."
        self.err_resp[idf.ERR][idf.ERR_DETAIL] = "Please add other device."
        self.err_resp[idf.ERR][idf.STATUS_CODE] = 500

        super(BaseException, self).__init__(self.err_resp, *args, **kwargs)






