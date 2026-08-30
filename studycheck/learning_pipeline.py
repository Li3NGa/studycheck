from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
from .document_parser import extract_text

class Mastery(str,Enum): NEW='new'; LEARNING='learning'; MASTERED='mastered'

@dataclass(frozen=True)
class KnowledgePoint:
    id:str; title:str; source:str

@dataclass(frozen=True)
class PracticeItem:
    knowledge_id:str; question:str; answer:str; source:str

@dataclass
class Progress:
    attempts:int=0; correct:int=0; streak:int=0
    @property
    def accuracy(self)->float:return self.correct/self.attempts if self.attempts else 0.0
    @property
    def mastery(self)->Mastery:
        if self.attempts>=3 and self.accuracy>=0.8:return Mastery.MASTERED
        if self.attempts:return Mastery.LEARNING
        return Mastery.NEW

def extract_knowledge(text:str,limit:int=30)->list[KnowledgePoint]:
    if not isinstance(text,str) or not text.strip(): raise ValueError('study text is required')
    if limit<1 or limit>100: raise ValueError('limit must be between 1 and 100')
    points=[]; seen=set()
    for line in text.splitlines():
        line=re.sub(r'^\s*(?:\d+[.、)]|[-*])\s*','',line).strip()
        if len(line)<4: continue
        title=line[:80]; key=title.casefold()
        if key in seen: continue
        seen.add(key); points.append(KnowledgePoint(f'K{len(points)+1:04d}',title,line))
        if len(points)>=limit: break
    return points

def build_practice(points:list[KnowledgePoint])->list[PracticeItem]:
    return [PracticeItem(p.id,f'请用自己的话解释：{p.title}',p.source,p.source) for p in points]

def grade_answer(progress:Progress,answer:str,expected:str)->dict:
    if not isinstance(answer,str) or not answer.strip(): raise ValueError('answer is required')
    if not isinstance(expected,str) or not expected.strip(): raise ValueError('expected answer is required')
    progress.attempts+=1
    correct=expected.casefold().strip() in answer.casefold().strip() or answer.casefold().strip() in expected.casefold().strip()
    if correct: progress.correct+=1; progress.streak+=1
    else: progress.streak=0
    return {'correct':correct,'attempts':progress.attempts,'accuracy':progress.accuracy,'streak':progress.streak,'mastery':progress.mastery.value}

def learning_cycle(text:str)->dict:
    points=extract_knowledge(text); practice=build_practice(points)
    return {'knowledge_points':[p.__dict__ for p in points],'practice':[p.__dict__ for p in practice],'total':len(points)}

def learning_cycle_from_file(path:str|Path,max_bytes:int=20_000_000)->dict:
    """Run the same deterministic learning pipeline against TXT/PDF/DOCX input."""
    return learning_cycle(extract_text(path,max_bytes))
