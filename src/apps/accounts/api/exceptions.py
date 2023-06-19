"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ErrorCode(enum.Enum):
    Not_Exists = "not_exists"
    Expired_OTP = "expired_OTP"
    Not_Authenticated = "not_authenticated"
    Permission_Denied = "permission_denied"
    Credential_Error = "credential_error"
    User_Not_Active = "user_not_active"
    Verified_OTP = "verified_OTP"
    Not_Similar_Passwords = "not_similar_passwords"
    Field_Error = "field_error"
    JWT_No_Type = "JWT_no_type"
    JWT_No_Id = "JWT_no_id"
    JWT_Wrong_Type = "JWT_wrong_type"
    JWT_token_not_valid = "token_not_valid"
    Bad_Authorization_Header = "bad_authorization_header"


class BaseError(APIException):
    """
    Base class for exceptions.
    Subclasses should provide `.detail_` and `.status_code` properties.
    """

    detail_ = None

    status_code = status.HTTP_200_OK

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code

        if detail is None:
            detail = self.detail_

        if code is None:
            code = self.status_code

        # For  failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def update_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        pass


class UserNotExistsError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The user does not exists.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class CredentialsError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Credential_Error.value,
        "detail": "Unable to log in with provided credentials.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotActiveResponse(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.User_Not_Active.value,
        "detail": "Account is inactive, please contact the admin",
    }
    status_code = status.HTTP_403_FORBIDDEN


class JWTAccessTokenNotExistsError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The access token does not exists in the header.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasNoType(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Type.value,
        "detail": "The access token has no type.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasWrongType(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_Wrong_Type.value,
        "detail": "The access token has wrong type.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasNoId(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Id.value,
        "detail": "The access token has no id.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasNoType(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Type.value,
        "detail": "The refresh token has no type.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasWrongType(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_Wrong_Type.value,
        "detail": "The refresh token has wrong type.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTRefreshTokenHasNoId(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Id.value,
        "detail": "The refresh token has no id.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenNotValid(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_token_not_valid.value,
        "detail": "Given access token not valid for any token type or expired.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTAuthenticationFailed(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Bad_Authorization_Header.value,
        "detail": "Authorization header must contain two space-delimited values.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class OTPNotExistsError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The OTP number does not exists.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class OTPExpiredError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Expired_OTP.value,
        "detail": "The OTP number has been expired, please resubmit your credential again.",
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class OTPVerifiedError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Verified_OTP.value,
        "detail": "The OTP number must be verified, please verify it first.",
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class NotAuthenticated(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Authenticated.value,
        "detail": "Authentication credentials were not provided.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Permission_Denied.value,
        "detail": "You do not have permission to perform this action.",
    }
    status_code = status.HTTP_403_FORBIDDEN


class NotSimilarPasswords(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Similar_Passwords.value,
        "detail": "The two password fields didn't match.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class SerializerFieldsError(BaseError):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Field_Error.value,
        "detail": "An error occurred in the fields",
        "data": {},
    }
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, errors, detail=None, code=None, status_code=None):
        self.update_data(errors=errors)
        super().__init__(detail, code, status_code)

    def update_data(self, **kwargs):
        errors = kwargs.get("errors")

        if errors:
            self.detail_["data"]["errors"] = errors
        return super().update_data(**kwargs)
