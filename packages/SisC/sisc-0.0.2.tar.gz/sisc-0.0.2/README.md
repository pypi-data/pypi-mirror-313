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
Both need to be manually installed.

## Usage

SisC provides a command line interface for easy usage.

Sisc currently best supports TEI XML as the input format. [Other formats](#supported-formats) are partially supported
and [more formats can easily be added](#adding-new-formats).

### Creating a Fingerprint

For XML files, two types of [masking](#masking) are available, `uniform` and `context`. A fingerprint with uniform
masking is created with:

~~~
sisc fingerprint uniform input_path output_path
~~~

If `input_path` is a folder, all files in that folder which are of the type specified with `--file-type` will be processed.
By default, `--file-type` is set to xml.

For TEI XML files, SisC supports moving footnotes to the end of the page if the TEI XML files contains annotations for
footnotes and page breaks. This can be useful when the footnotes are moved to their anchor position during annotation.
To turn on moving of footnotes, set `--move-notes`.

<details>
<summary>All command line options for uniform fingerprinting</summary>

~~~
usage: sisc fingerprint uniform [-h] [--file-type {txt,xml}]
                                [--move-notes | --no-move-notes]
                                [--add-quotation-marks | --no-add-quotation-marks]
                                [-s SYMBOL] [-k KEEP_COUNT] [-d DISTANCE]
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
  -k KEEP_COUNT, --keep-count KEEP_COUNT
                        Number of characters which not to mask.
  -d DISTANCE, --distance DISTANCE
                        The number of characters to mask between not masked
                        characters (default: 10)
~~~

</details>

#### Example

~~~
<TEI>
  <text>
    <body>
      <p>Some text with <q>an annotated quote</q>.</p>
    </body>
  </text>
</TEI>
~~~

The given simple TEI XML file would result in the following file with fingerprint with uniform masking:

~~~
<TEI>
  <text>
    <body sisc_start="0" sisc_end="36"><p sisc_start="1" sisc_end="35"><q sisc_start="16" sisc_end="34" /></p></body>
  </text>
  <standoff>
  S___ _ex_ ___h __ __no_____ q____.
  </standoff>
</TEI>
~~~

#### Masking

We currently support two types of masking: `Uniform` masking and `context` masking.  Uniform masking keeps a certain
number of characters, for example two, then masks a certain number of characters,  for example five, then keeps two
characters and so on. The result can be seen in the [example above](#example).

The number of characters to keep can be set with the `--keep-count` argument and the number of characters to mask with
`--distance`.

Context masking keeps the text around a specified tag unmasked and masked the rest of the text. The previous
[example](#example) with context masking would result in the following fingerprint:

~~~
____ text with __ _________ _____.
~~~

To specify the tag, use `--tag`. `--context-size` specify the context size on either side.
By default, the text of the tag itself is masked, to can be changed with `--keep-text`.

### Aligning Texts

To align PDF files with TEI XML fingerprints, run:

~~~
sisc align content_path fingerprint_path output_path
~~~

If `content_path` is a folder, all PDF and Txt files in that path will be processed. If `content_path` points to a file,
then `fingerprint_path` also needs to be a file. Otherwise, `fingerprint_path` needs to be a folder. In that case,
by default, SisC will look for XML files in `fingerprint_path`.

For annotations in external files, for example, json, `--annotation-type` can be set to `json` and `--annotation-path`
to the path with the annotation files.

<details>
<summary>All command line options for aligning texts</summary>

~~~
usage: sisc align [-h] [--annotation-path ANNOTATION_PATH]
                  [--annotation-type {txt,json}] [-f FIRST_PAGE]
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
  --annotation-type {txt,json}
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
                        Only used for json standoff annotations. Used to
                        specify json keys which represent a position and need
                        to be updated.
  --max-num-processes MAX_NUM_PROCESSES
                        Maximum number of processes to use for parallel
                        processing (default: 1).
  --max-text-length MAX_TEXT_LENGTH
                        The maximum length (in characters) of a text to align
                        (default: 200000).
~~~

</details>

## Supported Formats

TEI XML is the best supported format. Other formats, which have limited support, are txt and json.

To align a PDF file with a fingerprint stored in a Txt file and annotations in a json file, the following command can
be used:

~~~
sisc align path_to_file.pdf path_to_fingerprint.txt output_path --annotation-path path_to_file.json --annotation-type json --keys start end
~~~

For an annotation file, that looks something like the following example, this would update the start and end positions.

~~~
[
    {
        "text": "quote",
        "start": 5,
        "end": 10
    },
    {
        "text": "quote 2",
        "start": 25,
        "end": 32
    }
]
~~~

More fine-grained matching of keys is also possible, for example `key.start` will only match for `start` that appears
as a child of `key`.

## Custom Masking

To use custom masking, SisC needs to be run from code, for example:

~~~
from sisc.obfuscate.BaseObfuscater import BaseObfuscater
from sisc.fingerprint.TeiXmlFingerprinter import TeiXmlFingerprinter

class CustomObfuscater(BaseObfuscater):
    
    # overriding abstract method
    def obfuscate(self, text: str, positions: List[Tuple[int,int]]) -> str:
        ...

obfuscater = CustomObfuscater()
fingerprinter = TeiXmlFingerprinter(obfuscater)
result = fingerprinter.fingerprint(...)    
~~~

## Adding New Formats

To add support for a new file format, a custom fingerprinter and aligner can be implemented. For example:

~~~
from typing import Any, List
from sisc.fingerprint.BaseFingerprinter import BaseFingerprinter
from sisc.obfuscate.BaseObfuscater import BaseObfuscater
from sisc.alignment.BaseFileAligner import BaseFileAligner

class CustomFingerprinter(BaseFingerprinter[str, Any]):

    def __init__(self, obfuscater: BaseObfuscater):
        self.obfuscater = obfuscater

    # overriding abstract method
    def fingerprint(self, text: str, annotations: Any) -> str:
        return self.obfuscater.obfuscate(text, [])

class CustomAligner(BaseFileAligner[str]):

    # overriding abstract method
    def align(self, input_content: str, aligned_text: str, aligned_fingerprint: str, text_gap_positions: List[int],
              fingerprint_gap_positions: List[int]) -> str:
        ...

~~~

<!-- 

## Citation

Coming soon!

--->