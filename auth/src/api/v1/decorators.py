from typing import Callable, Dict, Union

from functools import wraps

from core.models import DefaultUserRole
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def superuser_required() -> Callable:  # type: ignore
    def wrapper(func) -> Callable:  # type: ignore
        @wraps(func)
        def decorator(*args, **kwargs) -> Union[Callable, Dict[str, str]]:  # type: ignore
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == DefaultUserRole.SUPERUSER.value:
                return func(*args, **kwargs)

            # TODO: вынести текст сообщения
            # TODO: сделать стандратный ответ
            return {"response": "super user only"}

        return decorator

    return wrapper
