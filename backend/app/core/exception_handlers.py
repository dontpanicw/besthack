# from fastapi import status

# class APIException(Exception):
#     """Базовый класс для всех исключений API"""
#     def __init__(self, status_code: int, message: str, details: dict = None):
#         self.status_code = status_code
#         self.message = message
#         self.details = details
#         super().__init__(message)

# class NotFoundException(APIException):
#     """Исключение при отсутствии запрашиваемого ресурса"""
#     def __init__(self, message: str, details: dict = None):
#         super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message, details=details)

# class BadRequestException(APIException):
#     """Исключение при неверном запросе"""
#     def __init__(self, message: str, details: dict = None):
#         super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, details=details)

# class UnauthorizedException(APIException):
#     """Исключение при неавторизованном доступе"""
#     def __init__(self, message: str = "Неавторизованный доступ", details: dict = None):
#         super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message, details=details)

# class ForbiddenException(APIException):
#     """Исключение при доступе к запрещенному ресурсу"""
#     def __init__(self, message: str = "Доступ запрещен", details: dict = None):
#         super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message, details=details) 