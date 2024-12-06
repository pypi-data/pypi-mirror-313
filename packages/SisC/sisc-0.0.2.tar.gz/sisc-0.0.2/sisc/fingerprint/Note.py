from dataclasses import dataclass
from xml.etree.ElementTree import Element


@dataclass
class Note:
    TYPE_FOOTNOTE = 1
    TYPE_ENDNOTE = 2

    type: int
    node: Element
    text: str
    next_page: bool = False
