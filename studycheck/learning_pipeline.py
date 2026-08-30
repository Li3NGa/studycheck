from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class KnowledgePoint:
    id:str
    title:str
    source:str

@dataclass(frozen=True)
class PracticeItem:
    knowledge_id:str
    question:str
    answer:str
    source:str

def extract_knowledge(text:str,limit:int=30)->list[KnowledgePoint]:
    if not isinstance(text,str) or not text.strip(): raise ValueError('study text is required')
    points=[]
    seen=set()
    for line in text.splitlines():
        line=re.sub(r'^\s*(?:\d+[.、)]|[-*])\s*','',line).strip()
        if len(line)<4: continue
        title=line[:80]
        key=title.casefold()
        if key in seen: continue
        seen.add(key); points.append(KnowledgePoint(f'K{len(points)+1:04d}',title,line))
        if len(points)>=limit: break
    return points

def build_practice(points:list[KnowledgePoint])->list[PracticeItem]:
    return [PracticeItem(p.id,f'请用自己的话解释：{p.title}',p.source,p.source) for p in points]

def learning_cycle(text:str)->dict:
    points=extract_knowledge(text)
    practice=build_practice(points)
    return {'knowledge_points':[p.__dict__ for p in points],'practice':[p.__dict__ for p in practice],'total':len(points)}
