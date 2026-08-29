from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

class OCRProvider(Protocol):
    def extract_text(self, image_bytes: bytes) -> str: ...

@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float

def extract_question(provider: OCRProvider, image_bytes: bytes) -> OCRResult:
    text=provider.extract_text(image_bytes).strip()
    if not text: raise ValueError("OCR returned empty text")
    return OCRResult(text=text, confidence=1.0)
