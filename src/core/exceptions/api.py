from rest_framework import status
from rest_framework.exceptions import APIException


class ApiBaseException(APIException):
    status_code = None
    default_detail = 'Detail'
    default_code = 'default code'

    def __init__(self, message=None, **kwargs):
        self.extra = kwargs

        if message is not None:
            self.default_detail = message

    @property
    def detail(self):
        return dict(
            self.extra,
            message=self.default_detail,
            type=self.__class__.__name__
        )


class BadRequestException(ApiBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request exception'
    default_code = 'bad request'


class ConflictException(ApiBaseException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Conflict exception'
    default_code = 'conflict'


class ForbiddenException(ApiBaseException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Forbidden exception'
    default_code = 'forbidden'


class PaymentRequiredException(ApiBaseException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment required exception'
    default_code = 'payment required'


class NotAcceptableException(ApiBaseException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Not acceptable exception'
    default_code = 'not acceptable'


class NotFoundException(ApiBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found exception'
    default_code = 'not found'


class PreconditionFailedException(ApiBaseException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_detail = 'Precondition failed exception'
    default_code = 'precondition failed'
