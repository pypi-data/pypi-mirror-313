# Readme

SisC is a tool to automatically separate  annotations from the underlying text. SisC uses a fingerprint, that is,
a masked version  of the text to merge stand-off annotations with another version of the original text, for example,
extracted from a PDF file. The fingerprint cannot be used on its own to recreate (meaningful parts of) the original
text and can therefore be shared.

## Installation

~~~
pip install sisc
~~~

## Dependencies

For PDF processing, SisC uses [pdf2image](https://github.com/Belval/pdf2image) and [Tesseract](https://github.com/tesseract-ocr/tesseract).
Both need to be installed. 

## Usage

SisC provides a command line interface for easy usage.

Sisc currently best supports TEI XML as the input format. [Other formats](#supported-formats) are partially supported
and [more formats can easily be added](#adding-new-formats).

### Creating a fingerprint

For XML files, two types of [masking](#masking) are available `uniform` and `context`. A fingerprint with uniform
masking is created with:

~~~
sisc fingerprint uniform input_path
~~~

If `input_path` is a folder, all files in that folder which are of the type specified in `file-type` will be processed.
By default, `file-type` is set to xml.

<details>
<summary>All command line options for uniform fingerprinting</summary>

~~~
usage: sisc fingerprint uniform [-h] [--file-type {txt,xml}]
                                [--move-notes | --no-move-notes]
                                [--add-quotation-marks | --no-add-quotation-marks]
                                [-s SYMBOL] [-d DISTANCE]
                                input-path output-path

Command to use uniform masking for the fingerprint.

positional arguments:
  input-path            Path to txt or xml file to create fingerprint from.
                        Can be a folder in which case all files will be
                        processed.
  output-path           Output folder path.

options:
  -h, --help            show this help message and exit
  --file-type {txt,xml}
                        The input file type to process. Only used when
                        input_path is a folder (default: xml).
  --move-notes, --no-move-notes
                        This will move footnotes and endnotes to the end of
                        their page/the whole text. Only works withXML file
                        which are annotated with footnotes/endnotes and
                        pagebreaks. (default: False)
  --add-quotation-marks, --no-add-quotation-marks
                        Add quotation marks in the fingerprint. Useful when
                        quotations marks are not present in the annotated XML
                        file. (default: False)
  -s SYMBOL, --symbol SYMBOL
                        The character to use for masking (default: _).
  -d DISTANCE, --distance DISTANCE
                        The number of characters to mask between not masked
                        characters (default: 10)
~~~

</details>

#### Masking

For TEI XML files, SisC supports moving footnotes to the end of the page if the TEI XML files contains annotations for
footnotes and page breaks. This can be useful when the footnotes are moved to their anchor position during annotation.
To turn on moving of footnotes, the command line option `--move-notes` can be used.

We currently support two types of masking: `Uniform` masking and `context` masking.

Uniform masking keeps a certain number of characters, for example two, then masks a certain number of characters,
for example five, then keeps two characters and so on. For example:

~~~
S___ _ex_ ___h __ __no_____ q____.
~~~

Context masking ... For example:

~~~
____ text with __ _________ _____.
~~~

### Aligning Texts

~~~
sisc align content_path fingerprint_path output_path
~~~

`content_path` can a file or folder, PDF or Txt
`fingerprint_path` TBD
`output_path` Folder to store the result

<details>
<summary>All command line options for aligning texts</summary>

~~~
usage: sisc align [-h] [--annotation-path ANNOTATION_PATH]
                  [--annotation-type {txt,json,xml}] [-f FIRST_PAGE]
                  [-l LAST_PAGE] [-k KEYS_TO_UPDATE [KEYS_TO_UPDATE ...]]
                  [--max-num-processes MAX_NUM_PROCESSES]
                  [--max-text-length MAX_TEXT_LENGTH]
                  content-path fingerprint-path output-path

Command to align fingerprint and PDF or text.

positional arguments:
  content-path          Path to the file (or folder) with the content for
                        alignment (txt or pdf).
  fingerprint-path      Path to the file (or folder) with the fingerprint
                        file(s) (txt or xml).
  output-path           Output folder path.

options:
  -h, --help            show this help message and exit
  --annotation-path ANNOTATION_PATH
                        Can be used to specify the path to the annotations.
                        Only needed when the annotations are not part of the
                        files specified in fingerprint_path.
  --annotation-type {txt,json,xml}
                        The type of the annotations to process. Only used when
                        content_path isa folder. (default: xml).
  -f FIRST_PAGE, --first-page FIRST_PAGE
                        Can be used to specify the first page to process. Only
                        used for PDF files and when processing a single PDF
                        file (default: 1).
  -l LAST_PAGE, --last-page LAST_PAGE
                        Can be used to specify the last page to process. Only
                        used for PDF files and when processing a single PDF
                        file (default: -1).
  -k KEYS_TO_UPDATE [KEYS_TO_UPDATE ...], --keys KEYS_TO_UPDATE [KEYS_TO_UPDATE ...]
                        TBD
  --max-num-processes MAX_NUM_PROCESSES
                        Maximum number of processes to use for parallel
                        processing (default: 1).
  --max-text-length MAX_TEXT_LENGTH
                        The maximum length (in characters) of a text to align
                        (default: 200000).
~~~

</details>

### Supported formats

TBD

### Adding new formats

Example coming soon!

<!---

### Evaluation

~~~
~~~

## Citation

Coming soon!

--->