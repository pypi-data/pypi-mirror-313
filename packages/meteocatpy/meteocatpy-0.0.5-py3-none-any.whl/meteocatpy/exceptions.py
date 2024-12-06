"""METEOCAT API exceptions."""

from __future__ import annotations

class MeteocatAPIError(Exception):
    """Clase base para todos los errores de la API de Meteocat."""
    def __init__(self, message: str, status_code: int, aws_info: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.aws_info = aws_info

class BadRequestError(MeteocatAPIError):
    """Error 400: Bad request."""
    def __init__(self, message: str, aws_info: dict = None):
        super().__init__(message, 400, aws_info)

class ForbiddenError(MeteocatAPIError):
    """Error 403: Forbidden."""
    def __init__(self, message: str, aws_info: dict = None):
        super().__init__(message, 403, aws_info)

class TooManyRequestsError(MeteocatAPIError):
    """Error 429: Too many requests."""
    def __init__(self, message: str, aws_info: dict = None):
        super().__init__(message, 429, aws_info)

class InternalServerError(MeteocatAPIError):
    """Error 500: Internal server error."""
    def __init__(self, message: str, aws_info: dict = None):
        super().__init__(message, 500, aws_info)

class UnknownAPIError(MeteocatAPIError):
    """Error desconocido de la API."""
    def __init__(self, message: str, status_code: int, aws_info: dict = None):
        super().__init__(message, status_code, aws_info)
