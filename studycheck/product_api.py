from __future__ import annotations
from pathlib import Path
from .content_workflow import ingest_content

def create_content(path:str|Path,title:str|None=None):
    return ingest_content(path,title)

def content_summary(content)->dict:
    return {'content_id':content.content_id,'title':content.title,'knowledge_points':content.knowledge_points,'text_length':len(content.text)}
