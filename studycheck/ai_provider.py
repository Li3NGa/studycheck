from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class GeneratedQuestion:
    knowledge_id:str
    question:str
    answer:str
    explanation:str
    source:str

class StudyAIProvider(Protocol):
    def generate(self,knowledge_id:str,title:str,source:str)->GeneratedQuestion: ...

class DeterministicProvider:
    """Safe MVP fallback. It only generates from supplied source text."""
    def generate(self,knowledge_id:str,title:str,source:str)->GeneratedQuestion:
        return GeneratedQuestion(knowledge_id,f'请根据资料解释：{title}',source,f'答案依据资料：{source}',source)
