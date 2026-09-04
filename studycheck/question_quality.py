from __future__ import annotations
from dataclasses import dataclass
from .ai_provider import GeneratedQuestion

QUESTION_TYPES={'true_false','single_choice','multiple_choice','short_answer'}

@dataclass(frozen=True)
class QualityDecision:
    accepted: bool
    difficulty: int
    reason: str

def assess_question(item: GeneratedQuestion, question_type: str = 'short_answer', difficulty: int = 3) -> QualityDecision:
    if question_type not in QUESTION_TYPES:
        return QualityDecision(False, difficulty, 'invalid question type')
    if not isinstance(difficulty, int) or not 1 <= difficulty <= 5:
        return QualityDecision(False, 3, 'difficulty must be between 1 and 5')
    try:
        text=' '.join((item.question,item.answer,item.explanation,item.source)).strip()
        if len(text) < 12:
            return QualityDecision(False, difficulty, 'question content is too short')
        if not item.knowledge_id.strip() or not item.source.strip():
            return QualityDecision(False, difficulty, 'question is missing source linkage')
    except AttributeError:
        return QualityDecision(False, difficulty, 'invalid generated question')
    return QualityDecision(True, difficulty, 'accepted')
