from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Protocol

@dataclass(frozen=True)
class GeneratedQuestion:
    knowledge_id: str
    question: str
    answer: str
    explanation: str
    source: str

class StudyAIProvider(Protocol):
    def generate(self, knowledge_id: str, title: str, source: str) -> GeneratedQuestion: ...

class DeterministicProvider:
    """Safe MVP fallback. It only generates from supplied source text."""
    def generate(self, knowledge_id: str, title: str, source: str) -> GeneratedQuestion:
        return GeneratedQuestion(knowledge_id, f'请根据资料解释：{title}', source, f'答案依据资料：{source}', source)

def validate_generated(item: GeneratedQuestion) -> GeneratedQuestion:
    if not item.knowledge_id.strip() or not item.question.strip() or not item.answer.strip():
        raise ValueError('generated question is incomplete')
    if not item.source.strip():
        raise ValueError('generated question must retain source')
    if len(item.question) > 2_000 or len(item.explanation) > 5_000:
        raise ValueError('generated question output is too large')
    return item

def generate_questions(points: Iterable, provider: StudyAIProvider) -> list[GeneratedQuestion]:
    results=[]
    for point in points:
        results.append(validate_generated(provider.generate(point.id, point.title, point.source)))
    return results
