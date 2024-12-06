"""HTTP exception"""


class BaseRPCException(Exception):
    r"""Base RPC exception.
    """
    pass


class BadRequestException(BaseRPCException):
    r""" BadRequestException represent HTTP Code 400.
    """
    pass


class ForbiddenException(BaseRPCException):
    r"""BadRequestException represent HTTP Code 403.
    """
    pass


class NotFoundException(BaseRPCException):
    r"""NotFoundException represent HTTP Code 404.
    """
    pass


class PreconditionFailedException(BaseRPCException):
    r"""PreconditionFailedException represent HTTP Code 412.
    """
    pass


class InternalServerErrorException(BaseRPCException):
    r"""InternalServerErrorException represent HTTP Code 500.
    """
    pass


class HTTPConnectionException(BaseRPCException):
    r"""HTTPConnectionException represent HTTP Connection error.
    """
    pass


class ModelNotSupportedException(BaseRPCException):
    r"""ModelNotSupportedException represent model is not supported
    """
    pass


class TypeNotSupportedException(BaseRPCException):
    r"""TypeNotSupportedException represent type is not supported
    """
    pass


class GZUServerException(BaseRPCException):
    r"""GZUServerException represent backend server failed response.
    """
    description: str = "Internal Server Error"
    code: int = 500

    def __init__(self, request_id="", code="", message="", service_err_code="", service_err_message=""):
        self.description = "request_id={}, code={}, message={}, service_err_code={}, service_err_message={} ".format(
            request_id, code, message, service_err_code, service_err_message)
        self.code = code if code else self.code

    def __str__(self):
        return self.description


class InvalidRequestArgumentError(BaseRPCException):
    r"""InvalidRequestArgumentError invalid request param
    """
    pass


class RiskInputException(BaseRPCException):
    r"""RiskInputException
    """
    pass