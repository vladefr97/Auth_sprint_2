from typing import Any, Callable, Coroutine

from functional.api.v1.conftest import HTTPResponse

AsyncRequest = Callable[[...], Coroutine[Any, Any, HTTPResponse]]
