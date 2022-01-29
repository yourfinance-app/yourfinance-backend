import traceback


class YFAException(Exception):
    http_status_code = 500
    message = "Unknown Error"
    error_code = "UNKNOWN_ERROR"
    data = dict()

    def as_dict(self):
        return dict(
            http_status_code=self.http_status_code,
            message=self.message, error_code=self.error_code,
            data=self.data or {}
        )


class UnknownError(YFAException):
    def __init__(self, e: Exception):
        self.error_code = "UNKNOWN_ERROR"
        self.http_status_code = 500
        self.message = "Unknown Error"
        self.data = dict(
            traceback=''.join(traceback.format_tb(e.__traceback__)),
            exc=str(e)
        )


class NotFound(YFAException):
    http_status_code = 404
    message = "Requested Entity Not Found"
    error_code = "NOT_FOUND"


class InvalidCountry(YFAException):
    http_status_code = 400
    message = "Invalid Country"
    error_code = "INVALID_COUNTRY"


class InvalidPassword(YFAException):
    http_status_code = 400
    message = "Invalid Password"
    error_code = "INVALID_PASSWORD"

    def __init__(self, result: dict = None) -> None:
        self.data = result


class DuplicateEntity(YFAException):
    http_status_code = 409
    message = "Duplicate Entity"
    error_code = "DUPLICATE_ENTITY"

    def __init__(self, entity_type: str, entity_value: str) -> None:
        self.data = dict(
            entity_type=entity_type,
            entity_value=entity_value
        )
