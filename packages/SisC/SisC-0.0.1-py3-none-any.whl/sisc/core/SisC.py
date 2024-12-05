import logging
from typing import Any, Optional

from Bio import Align
from sisc.alignment.BaseFileAligner import BaseFileAligner


def align_text(input_content: Any, text: str, fingerprint: str, base_aligner: Optional[BaseFileAligner],
               min_match_ratio: float = 0.0, max_text_length: int = 200000):

    if len(text) > max_text_length:
        logging.fatal('Text file too long')
        return None, None

    aligner = Align.PairwiseAligner()
    # TODO: make configurable
    aligner.match = 2
    aligner.open_gap_score = -3
    aligner.extend_gap_score = -1
    alignments = aligner.align(text, fingerprint)
    alignment = alignments[0]

    text_aligned = alignment[0]
    fingerprint_aligned = alignment[1]

    matched_count = 0
    total_count = 0
    for pos, char in enumerate(fingerprint_aligned):
        if char == 'x' or char == '-':
            continue

        if text_aligned[pos] == '-':
            continue

        total_count += 1

        if text_aligned[pos] == fingerprint_aligned[pos]:
            matched_count += 1

    matched_ratio = matched_count / total_count

    if matched_ratio < min_match_ratio:
        logging.warning(f'Low ratio of {matched_ratio}')
        return None, None

    text_gap_positions = [i for i, x in enumerate(alignment.indices[0]) if x == -1]
    fingerprint_gap_positions = [i for i, x in enumerate(alignment.indices[1]) if x == -1]

    aligner_result = None
    if base_aligner:
        aligner_result = base_aligner.align(input_content, alignment[0], alignment[1], text_gap_positions,
                                            fingerprint_gap_positions)

    return alignment[0], aligner_result
