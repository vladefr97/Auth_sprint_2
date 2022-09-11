from typing import Any, Union

from abc import ABC, abstractmethod


class BaseCache(ABC):
    def __init__(self, connection: Any):
        self.connection = connection

    @abstractmethod
    def get(self, key: str, **kwargs: str) -> Any:
        ...

    @abstractmethod
    def set_token(self, key: str, expire: int, value: Union[bytes, str]) -> None:
        ...

    @abstractmethod
    def pipeline(self, **kwargs: str) -> Any:
        ...
