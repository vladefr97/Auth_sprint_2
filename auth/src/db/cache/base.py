from typing import Union

from abc import ABC, abstractmethod


class BaseCache(ABC):
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set_token(self, key: str, expire: int, value: Union[bytes, str]):
        pass

    @abstractmethod
    def pipeline(self, **kwargs):
        pass
