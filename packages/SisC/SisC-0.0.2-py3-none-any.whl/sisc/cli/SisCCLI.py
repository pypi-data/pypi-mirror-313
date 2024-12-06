import errno
import json
import logging
import multiprocessing
import os
import statistics
import sys
from argparse import ArgumentParser, Action, BooleanOptionalAction
from os import listdir
from os.path import splitext, basename, join, isfile, isdir, exists
from typing import Optional, Any, List
from xml.etree import ElementTree

from kpcommons.Util import get_namespace

import sisc.core.SisC as SisC
import sisc.pdf.Pdf as Pdf
import sisc.util.Defaults as Defaults
from sisc.alignment.BaseFileAligner import BaseFileAligner
from sisc.alignment.JsonAligner import JsonAligner
from sisc.alignment.TxtAligner import TxtAligner
from sisc.alignment.TeiXmlAligner import TeiXmlAligner
from sisc.cli.NotSupportedException import NotSupportedException
from sisc.eval import Evaluation
from sisc.fingerprint.TextFingerprinter import TextFingerprinter
from sisc.fingerprint.TeiXmlFingerprinter import TeiXmlFingerprinter
from sisc.obfuscate.ContextObfuscater import ContextObfuscater
from sisc.obfuscate.UniformObfuscater import UniformObfuscater

from shutil import which

from sisc.pdf.TesseractException import TesseractException


class OptionValueCheckAction(Action):

    def __call__(self, parser, namespace, values, option_string=None):

        if option_string == '--max-num-processes':
            if int(values) <= 0:
                parser.error('{0} must be greater 0'.format(option_string))

        setattr(namespace, self.dest, values)


def __run_eval(eval_type: str, file_1_path: str, file_2_path: str, include_tags: List[str], exclude_tags: List[str]):
    average_distances = []

    if isfile(file_1_path) and isfile(file_2_path):
        filename = splitext(basename(file_1_path))[0]
        average_levenshtein = __eval_file(filename, eval_type, file_1_path, file_2_path, include_tags, exclude_tags)
        print(f'Average: {average_levenshtein:.2f}')
    elif isdir(file_1_path) and isdir(file_2_path):
        for file_or_folder in listdir(file_1_path):
            full_path = join(file_1_path, file_or_folder)
            filename = splitext(basename(full_path))[0]

            if isfile(full_path):
                full_path_2 = join(file_2_path, f'{filename}_aligned.xml')

                if exists(full_path_2):
                    average_levenshtein = __eval_file(filename, eval_type, full_path, full_path_2, include_tags,
                                                      exclude_tags)
                    average_distances.append(average_levenshtein)

        print(f'\n\nOverall average: {statistics.mean(average_distances):.2f}')


def __eval_file(filename: str, eval_type: str, file_1_path: str, file_2_path: str, include_tags: List[str],
                exclude_tags: List[str]):
    if eval_type == 'txt':
        with open(file_1_path, 'r', encoding='utf-8') as text_file:
            text_1 = text_file.read()

        with open(file_2_path, 'r', encoding='utf-8') as text_file:
            text_2 = text_file.read()

        Evaluation.eval_txt(text_1, text_2)
    elif eval_type == 'xml':
        element_tree_1 = ElementTree.parse(file_1_path)
        element_tree_2 = ElementTree.parse(file_2_path)
        average_levenshtein = Evaluation.eval_xml(filename, element_tree_1, element_tree_2,
                                                  include_tags, exclude_tags)
        return average_levenshtein
    elif eval_type == 'json':
        # TODO: eval json
        pass


def __align_file(input_path: str, fingerprint_path: str, annotation_path: str, output_path: str, key_to_update,
                 first_page, last_page, min_match_ratio, max_text_length) -> None:
    logging.getLogger().setLevel(logging.DEBUG)

    filename = splitext(basename(input_path))[0]
    logging.info(f'Aligning file {filename}')

    _, input_file_ext = splitext(input_path)

    if input_file_ext == '.txt':
        with open(input_path, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
    elif input_file_ext == '.pdf':
        text = Pdf.extract_text_from_pdf(input_path, first_page, last_page)
    else:
        return

    fingerprint: Optional[str] = None
    fingerprint_ext = splitext(fingerprint_path)[1]

    input_content: Any
    aligner:Optional[BaseFileAligner] = None

    if fingerprint_ext == '.txt':
        with open(fingerprint_path, 'r', encoding='utf-8') as fingerprint_file:
            fingerprint = fingerprint_file.read()
    elif fingerprint_ext == '.xml':
        input_content = ElementTree.parse(fingerprint_path)
        aligner = TeiXmlAligner()
        root = input_content.getroot()
        ns = get_namespace(root.tag)
        if ns:
            ElementTree.register_namespace('', ns[1:-1])
        fingerprint_node = root.find(f'.//{ns}standOff')

        if fingerprint_node is not None:
            fingerprint = fingerprint_node.text
            root.remove(fingerprint_node)
    else:
        return

    if not fingerprint:
        logging.error(f'Could not load fingerprint')
        return

    if annotation_path:
        annotation_ext = splitext(annotation_path)[1]

        if annotation_ext == '.json':
            with open(annotation_path, 'r', encoding='utf-8') as anno_file:
                json_input = anno_file.read()
            input_content = json.loads(json_input)
            aligner = JsonAligner(key_to_update)
        elif annotation_ext == '.txt':
            with open(annotation_path, 'r', encoding='utf-8') as anno_file:
                input_content = anno_file.read()
            aligner = TxtAligner()
        else:
            logging.error(f'Unexpected annotation format: {annotation_ext}')
            return

    al1, al2 = SisC.align_text(input_content, text, fingerprint, aligner, min_match_ratio=min_match_ratio,
                               max_text_length=max_text_length)

    if not al1:
        logging.error(f'Could not align {filename}')
        return

    with open(join(output_path, f'{filename}_aligned_content.txt'), 'w', encoding='utf-8') as out_file:
        out_file.write(al1)

    if al2 and annotation_path:
        annotation_ext = splitext(annotation_path)[1]
        if annotation_ext == '.txt':
            with open(join(output_path, f'{filename}_aligned_text.txt'), 'w', encoding='utf-8') as out_file:
                out_file.write(al2)
        elif annotation_ext == '.json':
            with open(join(output_path, f'{filename}_aligned.json'), 'w', encoding='utf-8') as out_file:
                out_file.write(json.dumps(al2))
        elif annotation_ext == '.xml':
            with open(join(output_path, f'{filename}_aligned.xml'), 'wb') as out_file:
                al2.write(out_file, encoding='utf-8', xml_declaration=True)


def __fingerprint_xml(text_file_path: str, output_path: str, fingerprint_type: str, symbol: str, move_notes: bool,
                      add_quotation_marks: bool, distance: int, keep_count: int, context_size: int, tag: str,
                      keep_text: bool):
    filename = splitext(basename(text_file_path))[0]
    element_tree = ElementTree.parse(text_file_path)

    if fingerprint_type == 'uniform':
        obfuscater = UniformObfuscater(symbol=symbol, keep_count=keep_count, distance=distance)
    elif fingerprint_type == 'context':
        obfuscater = ContextObfuscater(symbol=symbol, context_size=context_size, keep_text=keep_text)
    else:
        logging.fatal(f'Unknown fingerprint type: {fingerprint_type}')
        return

    fingerprinter = TeiXmlFingerprinter(obfuscater, move_notes=move_notes, add_quotation_marks=add_quotation_marks,
                                        keep_tag=tag)
    element_tree = fingerprinter.fingerprint(element_tree, None)

    with open(join(output_path, f'{filename}_fingerprint.xml'), 'wb') as out_file:
        element_tree.write(out_file, encoding='utf-8', xml_declaration=True)


def __fingerprint_txt(text_file_path: str, output_path: str, fingerprint_type: str, symbol:str, distance: int,
                      keep_count: int) -> None:
    filename = splitext(basename(text_file_path))[0]
    with open(text_file_path, 'r', encoding='utf-8') as text_file:
        text_1 = text_file.read()

    if fingerprint_type == 'uniform':
        obfuscater = UniformObfuscater(symbol=symbol, keep_count=keep_count, distance=distance)
    elif fingerprint_type == 'context':
        logging.error(f'Fingerprint type {fingerprint_type} is not supported for Txt files.')
        return
    else:
        logging.error(f'Unknown fingerprint type: {fingerprint_type}')
        return

    fingerprinter = TextFingerprinter(obfuscater)
    fingerprint = fingerprinter.fingerprint(text_1, None)

    with open(join(output_path, f'{filename}_fingerprint.txt'), 'w', encoding='utf-8') as out_file:
        out_file.write(fingerprint)


def __is_tesseract_available() -> bool:
    return which('tesseract') is not None


def main(argv=None):

    sisc_description = ('SisC is a tool to automatically separate  annotations from the underlying text. SisC uses a'
                        'fingerprint, that is, a masked version  of the text to merge stand-off annotations with'
                        'another version of the original text, for example, extracted from a PDF file. The fingerprint'
                        'cannot be used on its own to recreate (meaningful parts of) the original text and can'
                        'therefore be shared.')

    argument_parser = ArgumentParser(prog='sisc', description=sisc_description)

    argument_parser.add_argument('--log-level', dest='log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                           'CRITICAL'],
                                 help='Set the logging level (default: %(default)s)', default='WARNING')

    subparsers = argument_parser.add_subparsers(dest='top_subparser')
    subparsers.required = True

    fingerprint_parser_desc = 'Command to create a fingerprint.'
    parser_fingerprint = subparsers.add_parser('fingerprint', help=fingerprint_parser_desc,
                                               description=fingerprint_parser_desc)

    fingerprint_subparsers = parser_fingerprint.add_subparsers(dest='fingerprint_subparser')
    fingerprint_subparsers.required = True

    # uniform parser options
    input_path_help = ('Path to txt or xml file to create fingerprint from. Can be a folder in which case all files'
                       ' will be processed.')
    output_path_help = 'Output folder path.'
    file_type_help = 'The input file type to process. Only used when input_path is a folder (default: %(default)s).'
    move_notes_help = ('This will move footnotes and endnotes to the end of their page/the whole text. Only works with'
                       'XML file which are annotated with footnotes/endnotes and pagebreaks. (default: %(default)s)')
    add_quotation_marks_help = ('Add quotation marks in the fingerprint. Useful when quotations marks are not present in'
                                ' the annotated XML file. (default: %(default)s)')
    symbol_help = 'The character to use for masking (default: %(default)s).'


    uniform_parser_desc = 'Command to use uniform masking for the fingerprint.'
    parser_fingerprint_uniform = fingerprint_subparsers.add_parser('uniform', help=uniform_parser_desc,
                                                                   description=uniform_parser_desc)
    parser_fingerprint_uniform.add_argument('input_path', nargs=1, metavar='input-path',
                                            help=input_path_help)
    parser_fingerprint_uniform.add_argument('output_path', nargs=1, metavar='output-path',
                                            help=output_path_help)
    parser_fingerprint_uniform.add_argument('--file-type', dest='file_type', choices=['txt', 'xml'],
                                            default='xml', help=file_type_help)
    parser_fingerprint_uniform.add_argument('--move-notes', dest='move_notes', default=False,
                                            action=BooleanOptionalAction, help=move_notes_help)
    parser_fingerprint_uniform.add_argument('--add-quotation-marks', dest='add_quotation_marks',
                                            default=False, action=BooleanOptionalAction, help=add_quotation_marks_help)
    parser_fingerprint_uniform.add_argument('-s', '--symbol', type=str, dest='symbol',
                                            default=Defaults.DEFAULT_SYMBOL, help=symbol_help)
    parser_fingerprint_uniform.add_argument('-k', '--keep-count', type=int, dest='keep_count',
                                            default=Defaults.DEFAULT_KEEP_COUNT,
                                            help='Number of characters which not to mask.')
    parser_fingerprint_uniform.add_argument('-d', '--distance', type=int, dest='distance',
                                            default=Defaults.DEFAULT_DISTANCE,
                                            help='The number of characters to mask between not masked characters'
                                                 ' (default: %(default)d)')

    # context parser options
    context_parser_desc = 'Command to use context masking for the fingerprint.'

    parser_fingerprint_context = fingerprint_subparsers.add_parser('context', help=context_parser_desc,
                                                                   description=context_parser_desc)
    parser_fingerprint_context.add_argument('input_path', nargs=1, metavar='input-path',
                                            help=input_path_help)
    parser_fingerprint_context.add_argument('output_path', nargs=1, metavar='output-path',
                                            help=output_path_help)
    parser_fingerprint_context.add_argument('--file-type', dest='file_type', choices=['txt', 'xml'],
                                            default='xml', help=file_type_help)
    parser_fingerprint_context.add_argument('--move-notes', dest='move_notes', default=False,
                                            action=BooleanOptionalAction, help=move_notes_help)
    parser_fingerprint_context.add_argument('--add-quotation-marks', dest='add_quotation_marks', default=False,
                                            action=BooleanOptionalAction, help=add_quotation_marks_help)
    parser_fingerprint_context.add_argument('-s', '--symbol', type=str, dest='symbol',
                                            default=Defaults.DEFAULT_SYMBOL, help=symbol_help)
    parser_fingerprint_context.add_argument('-t', '--tag', type=str, dest='tag', required=True,
                                            help='The tag for which the surrounding context is not masked.')
    parser_fingerprint_context.add_argument('-c', '--context-size', type=int, dest='context_size',
                                            default=Defaults.DEFAULT_CONTEXT_SIZE,
                                            help='Size of the context window which is not masked (default: %(default)d)')
    parser_fingerprint_context.add_argument('-k', '--keep-text', dest='keep_text', default=False,
                                            action=BooleanOptionalAction,
                                            help='Do not mask the text of the tag itself. (default: %(default)s)')

    # Align Options
    align_parser_desc = 'Command to align fingerprint and PDF or text.'
    parse_align = subparsers.add_parser('align', help=align_parser_desc, description=align_parser_desc)

    parse_align.add_argument('content_path', nargs=1, metavar='content-path',
                             help='Path to the file (or folder) with the content for alignment (txt or pdf).')
    parse_align.add_argument('fingerprint_path', nargs=1, metavar='fingerprint-path',
                             help='Path to the file (or folder) with the fingerprint file(s) (txt or xml).')
    parse_align.add_argument('output_path', nargs=1, metavar='output-path',
                             help='Output folder path.')
    parse_align.add_argument('--annotation-path', type=str, dest='annotation_path',
                             help='Can be used to specify the path to the annotations. Only needed when the annotations'
                                  ' are not part of the files specified in fingerprint_path.', required=False)
    parse_align.add_argument('--annotation-type', choices=['txt', 'json'], dest='annotation_type',
                             default='xml', help='The type of the annotations to process. Only used when content_path is'
                                                 'a folder. (default: %(default)s).', required=False)
    parse_align.add_argument('-f', '--first-page', type=int, dest='first_page', default=1,
                             required=False, help='Can be used to specify the first page to process. Only used for PDF'
                                                  ' files and when processing a single PDF file (default: %(default)d).')
    parse_align.add_argument('-l', '--last-page', type=int, dest='last_page', default=-1,
                             required=False, help='Can be used to specify the last page to process. Only used for PDF'
                                                  ' files and when processing a single PDF file (default: %(default)d).')
    parse_align.add_argument('-k', '--keys', nargs='+', type=str, dest='keys_to_update',
                             required=False, help='Only used for json standoff annotations. Used to specify json keys'
                                                  ' which represent a position and need to be updated.')
    parse_align.add_argument('--max-num-processes', dest='max_num_processes', action=OptionValueCheckAction,
                             default=1, type=int,
                             help='Maximum number of processes to use for parallel processing (default: %(default)d).')
    # parse_align.add_argument('--min-match-ratio', dest='min_match_ratio', action=OptionValueCheckAction,
    #                          default=0.00, type=float, required=False)
    parse_align.add_argument('--max-text-length', dest='max_text_length', action=OptionValueCheckAction,
                             default=200000, type=int, required=False,
                             help='The maximum length (in characters) of a text to align (default: %(default)d).')

    # Eval options
    eval_parser_desc = 'Command to run the evaluation.'
    parse_eval = subparsers.add_parser('eval', help=eval_parser_desc, description=eval_parser_desc)

    parse_eval.add_argument('gold_path', nargs=1, metavar='gold_path',
                            help='Path to the file (or folder) with the gold/ground truth files.')
    parse_eval.add_argument('test_path', nargs=1, metavar='test_path',
                            help='Path the file or (folder) with the files to test.')
    parse_eval.add_argument('type', nargs=1, choices=['txt', 'json', 'xml'], metavar='type',
                            default='xml', help='The type of files to evaluate (default: %(default)s).')
    parse_eval.add_argument('-i', '--include-tags', nargs='+', type=str, dest='include_tags', required=False,
                            help='Only used for evaluation xml files. Can be used to specify tags which should be'
                                  ' included. If left empty, all tags will be included.')
    parse_eval.add_argument('-e', '--exclude-tags', nargs='+', type=str, dest='exclude_tags', required=False,
                            help='Only used for evaluation xml files. Can be used to specify tags which should be'
                                 ' excluded from the evaluation. If set, all matching tags and children will be excluded.')

    args = argument_parser.parse_args(argv)

    log_level = args.log_level
    logging.getLogger().setLevel(logging.getLevelName(log_level))

    if args.top_subparser == 'fingerprint':
        if args.fingerprint_subparser == 'uniform' or args.fingerprint_subparser == 'context':
            keep_count = 0
            distance = 0
            context_size = 0
            tag = ''
            keep_text = False
            fingerprint_type = args.fingerprint_subparser

            if args.fingerprint_subparser == 'uniform':
                input_path = args.input_path[0]
                output_path = args.output_path[0]
                file_type = args.file_type
                symbol = args.symbol
                move_notes = args.move_notes
                add_quotation_marks = args.add_quotation_marks
                keep_count = args.keep_count
                distance = args.distance
            elif args.fingerprint_subparser == 'context':
                input_path = args.input_path[0]
                output_path = args.output_path[0]
                file_type = args.file_type
                move_notes = args.move_notes
                symbol = args.symbol
                add_quotation_marks = args.add_quotation_marks
                context_size = args.context_size
                tag = args.tag
                keep_text = args.keep_text
            else:
                return

            if not exists(input_path):
                logging.fatal(f'Path does not exist: {input_path}')
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_path)

            if not exists(output_path):
                logging.fatal(f'Path does not exist: {output_path}')
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), output_path)

            if isfile(input_path):
                input_file_ext = splitext(input_path)[1]

                if input_file_ext == '.txt':
                    __fingerprint_txt(input_path, output_path, fingerprint_type, symbol, distance, keep_count)
                elif input_file_ext == '.xml':
                    __fingerprint_xml(input_path, output_path, fingerprint_type, symbol, move_notes,
                                      add_quotation_marks, distance, keep_count, context_size, tag, keep_text)
                else:
                    logging.fatal(f'Unsupported file extension: {input_file_ext}')
                    raise NotSupportedException(f'Unsupported file extension: {input_file_ext}')
            else:
                for file_or_folder in listdir(input_path):
                    full_path = join(input_path, file_or_folder)
                    if isfile(full_path):
                        input_file_ext = splitext(full_path)[1]
                        if input_file_ext == '.txt' and file_type == 'txt':
                            __fingerprint_txt(full_path, output_path, fingerprint_type, symbol, distance, keep_count)
                        elif input_file_ext == '.xml' and file_type == 'xml':
                            __fingerprint_xml(full_path, output_path, fingerprint_type, symbol, move_notes,
                                              add_quotation_marks, distance, keep_count, context_size, tag, keep_text)

    elif args.top_subparser == 'align':
        content_path = args.content_path[0]
        fingerprint_path = args.fingerprint_path[0]
        output_path = args.output_path[0]
        annotation_type = args.annotation_type
        annotation_path = args.annotation_path
        key_to_update = args.keys_to_update
        first_page = args.first_page
        last_page = args.last_page
        max_num_processes = args.max_num_processes
        # min_match_ratio = args.min_match_ratio
        max_text_length = args.max_text_length

        if isfile(content_path):
            input_file_ext = splitext(content_path)[1]
            if input_file_ext != '.txt' and input_file_ext != '.pdf':
                logging.fatal(f'Unsupported content file extension: {input_file_ext}')
                raise NotSupportedException(f'Unsupported file extension: {input_file_ext}')

            if input_file_ext == '.pdf' and not __is_tesseract_available():
                logging.fatal('Tesseract could not be found.')
                raise TesseractException('Could not find tesseract')

            fingerprint_ext = splitext(fingerprint_path)[1]

            if fingerprint_ext != '.xml' and fingerprint_ext != '.txt':
                logging.fatal(f'Unsupported fingerprint file extension: {fingerprint_ext}')
                raise NotSupportedException(f'Unsupported file extension: {fingerprint_ext}')

            if annotation_path:
                anno_file_ext = splitext(annotation_path)[1]
                if anno_file_ext != '.json' and anno_file_ext != '.txt':
                    logging.fatal(f'Unsupported annotation file extension: {anno_file_ext}')
                    raise NotSupportedException(f'Unsupported file extension: {anno_file_ext}')

            __align_file(content_path, fingerprint_path, annotation_path, output_path, key_to_update,
                         first_page, last_page, 0, max_text_length)
        else:
            if not isdir(fingerprint_path):
                logging.fatal('Fingerprint path is not a directory')
                raise FileNotFoundError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), fingerprint_path)

            if annotation_path and not isdir(annotation_path):
                logging.fatal(f'Annotation path is not a directory')
                raise FileNotFoundError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), annotation_path)

            found_pdf = False
            for file_name in listdir(content_path):
                if file_name.endswith('.pdf'):
                    found_pdf = True
                    break

            if found_pdf and not __is_tesseract_available():
                logging.fatal('Tesseract could not be found.')
                raise TesseractException('Could not find tesseract')

            pool = multiprocessing.Pool(max_num_processes)

            for file_or_folder in listdir(content_path):
                full_path = join(content_path, file_or_folder)

                if isfile(full_path):
                    filename = splitext(basename(full_path))[0]

                    if not annotation_path:
                        fingerprint_file_path = join(fingerprint_path, f'{filename}_fingerprint.xml')
                    else:
                        fingerprint_file_path = join(annotation_path, f'{filename}_fingerprint.txt')

                    annotation_file_path = None
                    if annotation_type == 'json':
                        annotation_file_path = join(annotation_path, f'{filename}.json')
                    elif annotation_type == 'txt':
                        annotation_file_path = join(annotation_path, f'{filename}.txt')

                    pool.apply_async(__align_file, args=(full_path, fingerprint_file_path, annotation_file_path, output_path,
                                                        key_to_update, 1, -1, 0, max_text_length))

            pool.close()
            pool.join()

    elif args.top_subparser == 'eval':
        eval_type = args.type[0]
        input_file_paths = args.input_file_paths
        file_1_path = input_file_paths[0]
        file_2_path = input_file_paths[1]
        include_tags = args.include_tags
        exclude_tags = args.exclude_tags

        __run_eval(eval_type, file_1_path, file_2_path, include_tags, exclude_tags)


if __name__ == '__main__':
    sys.exit(main())
