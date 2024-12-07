from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from typing import List

from aporia.sdk.client import Client


class BaseAporiaResource(ABC):
    @abstractclassmethod
    def create(cls, client: Client, name: str, *args, **kwargs) -> "BaseAporiaResource":
        ...

    @abstractclassmethod
    def read(cls, client: Client, id: str) -> "BaseAporiaResource":
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def delete(self):
        ...

    @abstractclassmethod
    def get_all(cls, client: Client, **kwargs) -> List["BaseAporiaResource"]:
        ...

    @abstractstaticmethod
    def delete_by_id(cls, client: Client, id: str):
        ...
