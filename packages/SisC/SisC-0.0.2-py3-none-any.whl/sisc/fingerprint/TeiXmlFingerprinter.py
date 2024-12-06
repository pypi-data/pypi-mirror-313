from typing import List, Tuple, Optional, Any

from sisc.fingerprint.BaseFingerprinter import BaseFingerprinter
from sisc.fingerprint.Note import Note
from sisc.obfuscate.BaseObfuscater import BaseObfuscater
from xml.etree.ElementTree import Element, ElementTree, SubElement
import xml.etree.ElementTree as ET
import re
from kpcommons.Util import get_namespace
from sisc.util import Constants


class TeiXmlFingerprinter(BaseFingerprinter[ElementTree, Any]):

    def __init__(self, obfuscater: BaseObfuscater, move_notes: bool = False, add_quotation_marks: bool = False,
                 keep_tag: str = ''):
        self.obfuscater = obfuscater
        self.move_notes = move_notes
        self.add_quotation_marks = add_quotation_marks
        self.keep_tag = keep_tag

    # overriding abstract method
    def fingerprint(self, input_content: ElementTree, annotations: Any) -> ElementTree:
        root = input_content.getroot()
        ns = get_namespace(root.tag)
        # TODO: support multiple namespaces
        if ns:
            ET.register_namespace('', ns[1:-1])
        body_elem = root.find(f'.//{ns}body')

        keep_tag_with_ns = f'{ns}{self.keep_tag}'

        text, _, tag_positions = self.__annotate_element(ns, body_elem, 0, [], False,
                                                         keep_tag_with_ns)
        text = self.obfuscater.obfuscate(text, tag_positions)

        fingerprint = SubElement(root, 'standOff')
        fingerprint.text = text

        return input_content

    def __annotate_element(self, ns: str, element: Element, prev_len: int, notes: List[Note], in_footnote: bool,
                           keep_tag: str):
        result: str = ''
        pb_pos: int = -1
        tag_positions: List[Tuple[int, int]] = []
        tag_start: int
        tag_end: int

        if element.tag == f'{ns}note':
            elem_note_type = element.attrib.get('type')

            if elem_note_type == 'footnote':
                in_footnote = True

        if self.move_notes and element.tag == f'{ns}pb':
            if in_footnote:
                pb_pos = prev_len

        tag_start = prev_len + len(result)
        element.set(Constants.ATTRIB_START, f'{prev_len + len(result)}')

        if self.add_quotation_marks and element.tag == f'{ns}q':
            result += '"'
            element.set(Constants.ATTRIB_OFFSET_START, '1')

        if element.text:
            text = element.text
            element.text = ''
            if text:
                result += self.__clean_text(text)

        for child in element:
            inner_text, inner_pb_pos, inner_tag_positions = self.__annotate_element(ns, child, prev_len + len(result),
                                                                                    notes, in_footnote, keep_tag)
            tag_positions.extend(inner_tag_positions)
            result += inner_text

            if inner_pb_pos != -1:
                pb_pos = inner_pb_pos

        if self.move_notes and element.tag == f'{ns}note':
            elem_note_type = element.attrib.get('type')

            if elem_note_type == 'endnote':
                notes.append(Note(Note.TYPE_ENDNOTE, element, result))
            else:
                if pb_pos == -1:
                    notes.append(Note(Note.TYPE_FOOTNOTE, element, result))
                else:
                    rel_pos = pb_pos - prev_len
                    notes.append(Note(Note.TYPE_FOOTNOTE, element, result[:rel_pos]))
                    notes.append(Note(Note.TYPE_FOOTNOTE, element, result[rel_pos:], True))

            tag_end = prev_len + len(result)
            element.set(Constants.ATTRIB_END, f'{prev_len + len(result)}')
            result = ''
        else:
            if self.add_quotation_marks and element.tag == f'{ns}q':
                result += '"'
                element.set(Constants.ATTRIB_OFFSET_END, '-1')

            tag_end = prev_len + len(result)
            element.set(Constants.ATTRIB_END, f'{prev_len + len(result)}')

        if self.move_notes and element.tag == f'{ns}pb':
            if not in_footnote:
                note_text = self.__add_notes(ns, Note.TYPE_FOOTNOTE, notes, prev_len + len(result))
                result += note_text
                element.set(Constants.ATTRIB_SKIP, f'{len(note_text)}')

        # TODO: make generic
        if self.move_notes and element.tag == f'{ns}body':
            note_text = self.__add_notes(ns,None, notes, prev_len + len(result))
            result += note_text
            tag_end = prev_len + len(result)
            element.set(Constants.ATTRIB_END, f'{prev_len + len(result)}')
            element.set(Constants.ATTRIB_SKIP, f'{len(note_text)}')

        # TODO: make generic
        if element.tag != f'{ns}body':
            text = element.tail
            element.tail = ''
            if text:
                result += self.__clean_text(text)

        if element.tag == keep_tag:
            tag_positions.append((tag_start, tag_end))

        return result, pb_pos, tag_positions

    def __add_notes(self, ns: str, note_type: Optional[str], notes, prev_len: int) -> str:
        result = ''
        clear = False
        for note in notes:
            if note_type and note.type != note_type:
                continue
            clear = True

            if note.next_page:
                continue

            page_length = -1
            if not Constants.ATTRIB_TEXT_START in note.node.attrib:
                text_start = prev_len + len(result)
                note.node.set(Constants.ATTRIB_TEXT_START, f'{text_start}')
            else:
                old_end = int(note.node.attrib[Constants.ATTRIB_TEXT_END])
                page_length = prev_len - old_end

            result += note.text
            text_end = prev_len + len(result)

            note.node.set(Constants.ATTRIB_TEXT_END, f'{text_end}')

            parent_start = int(note.node.attrib[Constants.ATTRIB_START])
            text_start = int(note.node.attrib[Constants.ATTRIB_TEXT_START])

            after_pb = False
            for sub_elem in note.node:
                sub_pb = self.__add_text_pos(ns, sub_elem, parent_start, text_start, page_length, after_pb)
                if sub_pb:
                    after_pb = True

        if clear:
            # modify list in-place
            notes[:] = [x for x in notes if x.next_page]
            for note in notes:
                note.next_page = False

        return result

    def __check_pb(self, ns: str, node: Element) -> bool:
        if node.tag == f'{ns}pb':
            return True

        for child in node:
            sub_pb = self.__check_pb(ns, child)

            if sub_pb:
                return True

        return False

    def __add_text_pos(self, ns: str, node: Element, parent_start: int, parent_text_start: int, page_length: int,
                       after_pb: bool) -> bool:
        contains_pb = self.__check_pb(ns, node)

        if Constants.ATTRIB_TEXT_START in node.attrib:
            if node.tag == f'{ns}pb':
                node.set(Constants.ATTRIB_SKIP, f'{page_length}')
                after_pb = True
            elif after_pb:
                old_start = int(node.attrib[Constants.ATTRIB_TEXT_START])
                new_start = old_start + page_length
                node.set(Constants.ATTRIB_TEXT_START, f'{new_start}')

                old_end = int(node.attrib[Constants.ATTRIB_TEXT_END])
                new_end = old_end + page_length
                node.set(Constants.ATTRIB_TEXT_END, f'{new_end}')
            elif contains_pb:
                old_start = int(node.attrib[Constants.ATTRIB_TEXT_START])
                old_end = int(node.attrib[Constants.ATTRIB_TEXT_END])
                if old_start < old_end:
                    new_end = old_end + page_length
                    node.set(Constants.ATTRIB_TEXT_END, f'{new_end}')
        else:
            node_start = int(node.attrib[Constants.ATTRIB_START])
            node_end = int(node.attrib[Constants.ATTRIB_END])
            diff_start = node_start - parent_start
            diff_end = node_end - parent_start

            node.set(Constants.ATTRIB_TEXT_START, f'{parent_text_start + diff_start}')
            node.set(Constants.ATTRIB_TEXT_END, f'{parent_text_start + diff_end}')

        for child in node:
            sub_after_pb = self.__add_text_pos(ns, child, parent_start, parent_text_start, page_length, after_pb)
            if sub_after_pb:
                after_pb = True

        return after_pb

    def __clean_text(self, text: str) -> str:
        result = re.sub(' *\n *', '\n', text, flags=re.DOTALL)
        return result