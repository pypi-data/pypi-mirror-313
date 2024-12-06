from typing import Any
from sisc.fingerprint.BaseFingerprinter import BaseFingerprinter
from sisc.obfuscate.BaseObfuscater import BaseObfuscater


class TextFingerprinter(BaseFingerprinter[str, Any]):

    def __init__(self, obfuscater: BaseObfuscater):
        self.obfuscater = obfuscater

    # overriding abstract method
    def fingerprint(self, text: str, annotations: Any) -> str:
        return self.obfuscater.obfuscate(text, [])