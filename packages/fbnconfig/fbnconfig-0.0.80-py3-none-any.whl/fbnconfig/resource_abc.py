from types import SimpleNamespace
from httpx import Client as httpxClient
from abc import ABC, abstractmethod
from typing import Dict, Any, Union, Optional, Sequence


class Ref(ABC):
    id: str

    @abstractmethod
    def attach(self, client: httpxClient) -> None:
        pass

    def deps(self):
        return []


class Resource(ABC):
    id: str

    @abstractmethod
    def read(self, client: httpxClient, old_state: SimpleNamespace) -> None|Dict[str,Any]:
        pass

    @abstractmethod
    def create(self, client: httpxClient) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, client: httpxClient, old_state) -> Union[None, Dict[str, Any]]:
        pass

    @staticmethod
    @abstractmethod
    def delete(client: httpxClient, old_state) -> None:
        pass

    @abstractmethod
    def deps(self) -> Sequence["Resource|Ref"]:
        pass
