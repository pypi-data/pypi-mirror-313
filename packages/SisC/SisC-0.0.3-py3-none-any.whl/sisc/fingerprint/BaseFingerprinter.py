from abc import ABC, abstractmethod
from typing import TypeVar, Generic, overload

T = TypeVar('T')
V = TypeVar('V')


class BaseFingerprinter(ABC, Generic[T, V]):

    @abstractmethod
    def fingerprint(self, input_content: T, annotations: V) -> T:
        pass