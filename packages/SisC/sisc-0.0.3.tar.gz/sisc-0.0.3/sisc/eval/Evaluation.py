from rapidfuzz.distance import Levenshtein
import statistics
import re


def eval_txt(text_1: str, text_2: str):
    matching_count = 0

    for c1, c2 in zip(text_1, text_2):

        if c1 == '-' or c2 == '-':
            matching_count += 1
        elif c1 == c2:
            matching_count += 1

    print(f'Ratio 1: {matching_count/len(text_1)}\nRatio 2: {matching_count/len(text_2)}')


def eval_xml(filename, element_tree_1, element_tree_2,  include_tags, exclude_tags):
    print(f'\n\n{filename}')
    ratios = __compare_element(element_tree_1.getroot(), element_tree_2.getroot(), include_tags, exclude_tags)
    print(f'\n\n-------------------------------------------------------'
          f'\nAverage Levenshtein distance: {statistics.mean(ratios):.2f}'
          f'\n-------------------------------------------------------')

    return statistics.mean(ratios)


def __compare_element(element_1, element_2, include_tags, exclude_tags):
    assert len(element_1) == len(element_2)
    assert element_1.tag == element_2.tag
    ratios = []

    if not include_tags or element_1.tag in include_tags:
        text_1 = __get_text(element_1)
        text_2 = __get_text(element_2)

        if not text_1:
            text_1 = ''

        if not text_2:
            text_2 = ''

        text_1 = re.sub(r'\W', '', text_1, flags=re.DOTALL)
        text_2 = re.sub(r'\W', '', text_2, flags=re.DOTALL)
        ratio = Levenshtein.normalized_similarity(text_1, text_2)
        ratios.append(ratio)

        if ratio < 0.00:
            print(f'{text_1} -- {text_2}\n{ratio}')

        return ratios

    # exclude footnotes
    if not exclude_tags or element_1.tag not in exclude_tags:
        for child_1, child_2 in zip(element_1, element_2):
            sub_ratios = __compare_element(child_1, child_2, include_tags, exclude_tags)
            ratios.extend(sub_ratios)

    return ratios

def __get_text(element):

    result = ''
    if element.text:
        text = element.text
        result += text

    for child in element:
        result += __get_text(child)

    if element.tail:
        result += element.tail

    return result
