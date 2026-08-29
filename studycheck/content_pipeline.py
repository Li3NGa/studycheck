from __future__ import annotations
import re
from pathlib import Path
from .content_parser import extract_text

def extract_knowledge_points(path:str|Path,limit:int=50)->list[str]:
    text=extract_text(path)
    points=[]
    seen=set()
    for line in text.splitlines():
        value=re.sub(r'^[\s#\-\d.、]+','',line).strip()
        if len(value)<4 or len(value)>120: continue
        if value not in seen:
            seen.add(value); points.append(value)
        if len(points)>=limit: break
    return points
