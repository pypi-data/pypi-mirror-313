import logging
import subprocess
import tempfile
from errno import ENOENT
from os.path import join
from typing import List
from pdf2image import convert_from_path
from PIL import Image

from sisc.pdf.TesseractException import TesseractException


def extract_text_from_pdf(pdf_path: str, first_page: int = 1, last_page: int = -1) -> str:
    __check_page_range(first_page, last_page)
    pages = __extract_pages_from_pdf(pdf_path)
    text = __run_tesseract(pages, first_page, last_page)
    return text

def __check_page_range(first_page: int, last_page: int):
    if first_page < 1:
        raise ValueError(f'Invalid page: {first_page}')

    if last_page > -1 and 0 < last_page < first_page:
        raise ValueError(f'Invalid page range: {first_page} to {last_page}')

def __extract_pages_from_pdf(pdf_path: str, ) -> List[Image.Image]:
    pages = convert_from_path(pdf_path, 300)
    return pages

def __run_tesseract(pages: List[Image.Image], first_page, last_page) -> str:
    output_text = ''
    page_count = len(pages)
    img_extension = 'PNG'

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.debug(f'created temporary directory {temp_dir}')

        for pos, page in enumerate(pages):
            if pos < first_page - 1:
                logging.info(f'Skipping page {pos+1}/{page_count}')
                continue

            if last_page > 0 and pos > last_page - 1:
                logging.info(f'Skipping page {pos+1}/{page_count}')
                continue

            # logging.info(f'OCR page {pos+1}/{page_count}')

            image_file_name = join(temp_dir, f'page_{pos+1}.{img_extension}')
            page.save(image_file_name, format=img_extension, **page.info)

            try:
                p_result = subprocess.run(['tesseract', image_file_name, '-', '-l', 'deu', '--dpi', '300'], capture_output=True)
            except OSError as e:
                if e.errno != ENOENT:
                    raise
                else:
                    raise TesseractException('Could not find tesseract')

            if p_result.returncode != 0:
                logging.error(f'Could not read page {pos+1}')
                continue

            out = p_result.stdout.decode('utf-8')

            if output_text:
                output_text += '\n'

            output_text += out

    return output_text
