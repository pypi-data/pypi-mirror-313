from typing import List
from xml.etree.ElementTree import ElementTree
from sisc.alignment.BaseFileAligner import BaseFileAligner
from sisc.util import Constants


class TeiXmlAligner(BaseFileAligner[ElementTree]):

    # overriding abstract method
    def align(self, input_content: ElementTree, aligned_text: str, aligned_fingerprint: str,
              text_gap_positions: List[int], fingerprint_gap_positions: List[int]) -> ElementTree:
        root = input_content.getroot()
        self.__update_element(root, fingerprint_gap_positions, aligned_text, -1, False)
        return input_content

    def __update_element(self, element, fingerprint_gap_positions: List[int], aligned_text, next_end, parent_moved_text):

        if not Constants.ATTRIB_START in element.attrib or not Constants.ATTRIB_END in element.attrib:
            for child in element:
                self.__update_element(child, fingerprint_gap_positions, aligned_text, -1, parent_moved_text)
            return

        start_attrib = Constants.ATTRIB_START
        end_attrib = Constants.ATTRIB_END

        moved_text = False
        if Constants.ATTRIB_TEXT_START in element.attrib:
            start_attrib = Constants.ATTRIB_TEXT_START
            end_attrib = Constants.ATTRIB_TEXT_END
            moved_text = True

        start = int(element.attrib[start_attrib])
        start = self.__calculate_new_value(start, fingerprint_gap_positions)
        end = int(element.attrib[end_attrib])
        end = self.__calculate_new_value(end, fingerprint_gap_positions)

        offset_start = 0
        offset_end = 0
        if Constants.ATTRIB_OFFSET_START in element.attrib:
            offset_start = int(element.attrib[Constants.ATTRIB_OFFSET_START])
        if Constants.ATTRIB_OFFSET_END in element.attrib:
            offset_end = int(element.attrib[Constants.ATTRIB_OFFSET_END])

        # TODO: make generic
        # special case for last element
        if element.tag == 'body' and Constants.ATTRIB_SKIP in element.attrib:
            skip_length = int(element.attrib.get(Constants.ATTRIB_SKIP))
            end -= skip_length

        if len(element) > 0:
            child_start = int(element[0].attrib[start_attrib])
            child_start = self.__calculate_new_value(child_start, fingerprint_gap_positions)
            element.text = aligned_text[start + offset_start:child_start]

            for child_pos, child in enumerate(element):
                if child_pos + 1 < len(element):
                    temp_next_end = int(element[child_pos + 1].attrib[start_attrib])
                    temp_next_end = self.__calculate_new_value(temp_next_end, fingerprint_gap_positions)
                else:
                    temp_next_end = end + offset_end

                self.__update_element(child, fingerprint_gap_positions, aligned_text, temp_next_end, moved_text)
        else:
            element.text = aligned_text[start + offset_start:end + offset_end]

        if next_end > -1:
            # handle pagebreaks in footnotes and elements spanning over footnotes, i.e., elements with pagebreaks and
            # move_text == True
            if Constants.ATTRIB_SKIP in element.attrib:
                skip_cnt = int(element.attrib[Constants.ATTRIB_SKIP])
                child_real_end = end + skip_cnt
                element.tail = aligned_text[child_real_end:next_end]
            elif not parent_moved_text and moved_text:
                child_real_end = int(element.attrib[Constants.ATTRIB_START])
                child_real_end = self.__calculate_new_value(child_real_end, fingerprint_gap_positions)
                element.tail = aligned_text[child_real_end:next_end]
            else:
                element.tail = aligned_text[end:next_end]

        element.attrib.pop(Constants.ATTRIB_START, None)
        element.attrib.pop(Constants.ATTRIB_END, None)
        element.attrib.pop(Constants.ATTRIB_TEXT_START, None)
        element.attrib.pop(Constants.ATTRIB_TEXT_END, None)
        element.attrib.pop(Constants.ATTRIB_SKIP, None)
        element.attrib.pop(Constants.ATTRIB_OFFSET_START, None)
        element.attrib.pop(Constants.ATTRIB_OFFSET_END, None)

    def __calculate_new_value(self, value: int, fingerprint_gap_positions: List[int]) -> int:
        count_before = self.__count_before(value, fingerprint_gap_positions)
        return value + count_before

    @staticmethod
    def __count_before(value, gap_positions: List[int]) -> int:
        count_before = 0
        for pos in gap_positions:
            if pos < value + count_before:
                count_before += 1
            else:
                break

        return count_before
