from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')


class BaseFileAligner(ABC, Generic[T]):

    @abstractmethod
    def align(self, input_content: T, aligned_text: str, aligned_fingerprint: str, text_gap_positions: List[int],
              fingerprint_gap_positions: List[int]) -> T:
        """
        TBD
        :param input_content:
        :param aligned_text:
        :param aligned_fingerprint:
        :param text_gap_positions:
        :param fingerprint_gap_positions:
        :return:
        """
        pass