from typing import List, Tuple

from sisc.obfuscate.BaseObfuscater import BaseObfuscater
from sisc.util import Defaults
import re


class ContextObfuscater(BaseObfuscater):

    def __init__(self, symbol: str = Defaults.DEFAULT_SYMBOL, context_size: int = Defaults.DEFAULT_CONTEXT_SIZE,
                 keep_text: bool = False):
        self.symbol = symbol
        self.context_size = context_size
        self.keep_text = keep_text

    # overriding abstract method
    def obfuscate(self, text: str, positions: List[Tuple[int,int]]) -> str:
        text_list = list(text)

        for c_pos in range(len(text_list)):
            in_range = False
            for pos in positions:
                if c_pos < pos[0] - self.context_size:
                    break

                if self.keep_text:
                    if pos[0] - self.context_size <= c_pos <= pos[1] + self.context_size:
                        in_range = True
                        break
                else:
                    if (pos[0] - self.context_size <= c_pos < pos[0]) or (pos[1] <= c_pos <= pos[1] + self.context_size):
                        in_range = True
                        break

            if not in_range:
                if not re.match(r'\W', text_list[c_pos]):
                    text_list[c_pos] = self.symbol

        return ''.join(text_list)