import warnings

from .dataclasses import Response


class HttpException(Exception):
    def __init__(self, **kwargs):
        """
        :key message: (detailed) error message
        :key status_code: HTTP status code
        :key error_code: Short error description
        :key extra: Dictionary of extra information
        """
        super().__init__()

        self.message = kwargs.get('message', 'An unknown error has occurred')
        self.status_code = kwargs.get('status_code', 500)
        self.code = kwargs.get('error_code', "Internal Server Error")
        self.extra = kwargs.get('extra')

    def __str__(self):
        return f'{self.status_code} {self.code}: {self.message}'

    def to_response(self) -> Response:
        return Response(
            status_code=self.status_code,
            body=f'{self.code}: {str(self)}',
            headers={'Content-Type': 'text/plain'},
            extra=self.extra,
        )


class BadRequestException(HttpException):
    def __init__(self, **kwargs):
        super().__init__(status_code=400, error_code='Bad Request', **kwargs)


class MissingInputException(BadRequestException):
    """Exception raised when one of the necessary inputs is missing."""

    def __init__(self, **kwargs):
        """
        See keys of :class:`HttpException`.

        :key scopes: scope missing from user input
        """
        scopes: list[str] = kwargs.get('scopes', [])
        msg = f"Missing input variable(s): [{', '.join(iter(kwargs.get('scopes', [])))}]"
        super().__init__(message=msg, extra={'scopes': scopes}, **kwargs)


class IncorrectVolumeException(BadRequestException):
    """Exception raised when user input has incorrect volume."""

    def __init__(self, **kwargs):
        """
        See keys of :class:`HttpException`.

        :key val: Incorrect volume value
        """
        val = kwargs.get('val')
        msg = f"Incorrect volume entered ({val}). Please enter a positive value."
        MissingInputException()
        super().__init__(message=msg, extra={'volume': val}, **kwargs)


class NotFoundException(HttpException):
    def __init__(self, message, **kwargs):
        super().__init__(status_code=404, error_code='Not Found', message=message, **kwargs)


class DataNotFoundException(NotFoundException):
    """Exception raised when one of the necessary input by the user is missing from the dataset."""

    def __init__(self, **kwargs):
        """
        See keys of :class:`HttpException`.

        :key key: column/scope with missing data
        :key value: data value that is missing
        """
        key = kwargs.get('key', "Unknown")
        value = kwargs.get('value', "Unknown")
        msg = f"Data point not found in dataset for column '{key}' (with value '{value}')"
        extra = {'key': key, 'value': value}
        super().__init__(message=msg, extra=extra, **kwargs)


class InvalidStateException(HttpException):
    """Exception raised when an invalid / conflicting state is encountered."""

    def __init__(self, message, **kwargs):
        """
        See keys of :class:`HttpException`.
        """
        super().__init__(status_code=409, error_code='Conflict', message=message, **kwargs)


class MissingRepresentationException(InvalidStateException):
    """Exception raised when the script expects a representation, but no such scope exists in the dataset."""

    def __init__(self, **kwargs):
        """
        See keys of :class:`HttpException`.

        :key val: column that should be indicated as a representation
        """
        val = kwargs.get('val')
        msg = "Unable to find representation. Please update scopes file."
        super().__init__(message=msg, extra={'column': val}, **kwargs)


class RateLimitException(HttpException):
    def __init__(self, status_code=429, error_code='Too Many Requests', message=None, **kwargs):
        self.reset_at = kwargs.get('reset_at')
        msg = message if not None else f"Rate limit reached. Reset at: '{self.reset_at or 'Unknown'}'."
        extra = {'reset_at': self.reset_at}
        super().__init__(status_code=status_code, error_code=error_code, message=msg, extra=extra, **kwargs)


class PriceCypherError(HttpException):
    def __init__(self, status_code, error_code, message):
        warnings.warn('Use of the class `PriceCypherError` is deprecated. Please use `HttpException` instead.')
        super().__init__(message=message, status_code=status_code, error_code=error_code)


class RateLimitError(PriceCypherError):
    def __init__(self, error_code=429, message=None, reset_at=None):
        warnings.warn('Use of the class `RateLimitError` is deprecated. Please use `RateLimitException` instead.')
        self.reset_at = reset_at
        super().__init__(status_code=error_code, error_code='Too Many Requests', message=message)
