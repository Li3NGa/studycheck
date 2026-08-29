from __future__ import annotations
from pathlib import Path

class ContentParseError(ValueError): pass

def extract_text(path:str|Path)->str:
    p=Path(path)
    if not p.exists(): raise ContentParseError('content not found')
    if p.suffix.lower()=='.txt': return p.read_text(encoding='utf-8')
    if p.suffix.lower()=='.docx':
        try:
            from docx import Document
        except ImportError as exc: raise ContentParseError('DOCX support requires python-docx') from exc
        return '\n'.join(x.text for x in Document(str(p)).paragraphs if x.text).strip()
    if p.suffix.lower()=='.pdf':
        try:
            from pypdf import PdfReader
        except ImportError as exc: raise ContentParseError('PDF support requires pypdf') from exc
        return '\n'.join(page.extract_text() or '' for page in PdfReader(str(p)).pages).strip()
    raise ContentParseError(f'unsupported content type: {p.suffix}')
