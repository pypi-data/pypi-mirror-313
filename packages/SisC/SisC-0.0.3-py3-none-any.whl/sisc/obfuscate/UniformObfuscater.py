from typing import List, Tuple

from sisc.obfuscate.BaseObfuscater import BaseObfuscater
from sisc.util import Defaults
import re


class UniformObfuscater(BaseObfuscater):

    def __init__(self, symbol: str = Defaults.DEFAULT_SYMBOL, keep_count: int = Defaults.DEFAULT_KEEP_COUNT,
                 distance: int = Defaults.DEFAULT_DISTANCE):
        self.symbol = symbol
        self.keep_count = keep_count
        self.distance = distance

    # overriding abstract method
    def obfuscate(self, text: str, positions: List[Tuple[int,int]]) -> str:
        text_list = list(text)

        show_count = self.keep_count
        hide_count = self.distance

        for pos in range(len(text_list)):

            if show_count > 0:
                show_count -= 1
            elif hide_count > 0:
                hide_count -= 1

                if not re.match(r'\W', text_list[pos]):
                    text_list[pos] = self.symbol

            if show_count == 0 and hide_count == 0:
                show_count = self.keep_count
                hide_count = self.distance

        return ''.join(text_list)