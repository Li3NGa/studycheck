from __future__ import annotations
from pathlib import Path
from .content_parser import extract_text
from .content_pipeline import extract_knowledge_points
from .content_models import LearningContent

def ingest_content(path:str|Path,title:str|None=None)->LearningContent:
    text=extract_text(path)
    if not text.strip(): raise ValueError('learning content contains no extractable text')
    return LearningContent(title or Path(path).stem,text,extract_knowledge_points(path))
