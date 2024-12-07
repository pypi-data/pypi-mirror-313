from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Tuple

from aporia.sdk.client import Client


class NonDeletableResourceException(Exception):
    pass


class CompareStatus(Enum):
    SAME = "same"
    UPDATEABLE = "updateable"
    MISMATCHED = "mismatched"


class BaseResource(ABC):
    @abstractmethod
    def __init__(self, resource_name: str, /, **kwargs):
        ...

    @abstractmethod
    def compare(self, resource_data: Dict) -> CompareStatus:
        ...

    @abstractmethod
    def setarg(self, arg_name: str, arg_value: Any):
        ...

    @abstractmethod
    def create(self, client: Client) -> Tuple[str, Dict]:
        ...

    @abstractmethod
    def read(self, client: Client, id: str) -> Dict:
        ...

    @abstractmethod
    def update(self, client: Client, id: str) -> Dict:
        ...

    @abstractmethod
    def delete(self, client: Client, id: str):
        ...

    @abstractmethod
    def get_diff(self, resource_data: Dict) -> Dict:
        ...
