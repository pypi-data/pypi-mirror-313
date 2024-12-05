from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseObfuscater(ABC):

    @abstractmethod
    def obfuscate(self, text: str, positions: List[Tuple[int,int]]) -> str:
        pass
