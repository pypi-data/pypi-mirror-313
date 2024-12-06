from typing import List
from sisc.alignment.BaseFileAligner import BaseFileAligner


class TxtAligner(BaseFileAligner[str]):

    # overriding abstract method
    def align(self, input_content: str, aligned_text: str, aligned_fingerprint: str, text_gap_positions: List[int],
              fingerprint_gap_positions: List[int]) -> str:
        result = ''
        for c in input_content:

            found_gap = True
            while found_gap:
                if len(result) in fingerprint_gap_positions:
                    result += '-'
                else:
                    found_gap = False

            result += c

        return result
