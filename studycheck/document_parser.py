from __future__ import annotations
from pathlib import Path

class DocumentParseError(ValueError): pass
SUPPORTED={'.txt','.pdf','.docx'}

def extract_text(path:str|Path,max_bytes:int=20_000_000)->str:
    p=Path(path)
    if max_bytes<=0: raise ValueError('max_bytes must be positive')
    if not p.is_file(): raise DocumentParseError('document not found')
    if p.stat().st_size>max_bytes: raise DocumentParseError('document exceeds size limit')
    suffix=p.suffix.lower()
    if suffix not in SUPPORTED: raise DocumentParseError(f'unsupported document type: {suffix}')
    try:
        if suffix=='.txt': text=p.read_text(encoding='utf-8')
        elif suffix=='.pdf': text=_pdf(p)
        else: text=_docx(p)
    except UnicodeDecodeError as exc: raise DocumentParseError('text document must be UTF-8') from exc
    if not text.strip(): raise DocumentParseError('document is empty')
    return text

def _pdf(path:Path)->str:
    try:
        from pypdf import PdfReader
        return '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages).strip()
    except Exception as exc: raise DocumentParseError('failed to parse PDF') from exc

def _docx(path:Path)->str:
    try:
        from docx import Document
        return '\n'.join(p.text for p in Document(str(path)).paragraphs if p.text).strip()
    except Exception as exc: raise DocumentParseError('failed to parse DOCX') from exc
