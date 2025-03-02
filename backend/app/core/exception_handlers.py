from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

class APIException(Exception):
    """Базовый класс для всех исключений API"""
    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(message)

class NotFoundException(APIException):
    """Исключение при отсутствии запрашиваемого ресурса"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message, details=details)

class BadRequestException(APIException):
    """Исключение при неверном запросе"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, details=details)

class UnauthorizedException(APIException):
    """Исключение при неавторизованном доступе"""
    def __init__(self, message: str = "Неавторизованный доступ", details: dict = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message, details=details)

class ForbiddenException(APIException):
    """Исключение при доступе к запрещенному ресурсу"""
    def __init__(self, message: str = "Доступ запрещен", details: dict = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message, details=details)

async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Обработчик для пользовательских исключений API"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Обработчик для ошибок валидации запросов"""
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Ошибка валидации данных",
                "details": {
                    "errors": [
                        {
                            "loc": ".".join(str(loc) for loc in err["loc"]) if isinstance(err["loc"], tuple) else err["loc"],
                            "msg": err["msg"],
                            "type": err["type"]
                        } for err in errors
                    ]
                }
            }
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Обработчик для ошибок базы данных"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Ошибка базы данных"
    
    if isinstance(exc, IntegrityError):
        status_code = status.HTTP_409_CONFLICT
        message = "Конфликт данных"
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": status_code,
                "message": message,
                "details": {"error": str(exc)}
            }
        }
    )

async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Обработчик для общих исключений"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Внутренняя ошибка сервера",
                "details": {"error": str(exc)}
            }
        }
    )

def add_exception_handlers(app: FastAPI) -> None:
    """Добавляет все обработчики исключений к приложению"""
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, internal_exception_handler) 