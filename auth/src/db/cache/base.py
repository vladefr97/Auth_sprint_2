from abc import ABC, abstractmethod


class BaseCache(ABC):
    def __init__(self, connection: any):
        self.connection = connection

    @abstractmethod
    def get(self, key: str, **kwargs: str) -> any:
        ...

    @abstractmethod
    def set_token(self, key: str, expire: int, value: dict[bytes, str]) -> None:
        ...

    @abstractmethod
    def pipeline(self, **kwargs: str) -> any:
        ...
