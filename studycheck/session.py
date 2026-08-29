from __future__ import annotations
from datetime import datetime
from .knowledge import KnowledgeGraph
from .learning_update import apply_review
from .review_queue import build_daily_queue

def start_session(graph: KnowledgeGraph, now: datetime | None = None, limit: int = 20) -> list[dict]:
    return build_daily_queue(graph, now, limit)

def finish_review(graph: KnowledgeGraph, knowledge_point: str, correct: bool, transfer: bool = False) -> dict:
    evidence=graph.add(knowledge_point)
    apply_review(evidence, correct, transfer)
    return {"knowledge_point":knowledge_point,"mastery":evidence.mastery.value,"accuracy":evidence.accuracy,"attempts":evidence.attempts,"transfer_passes":evidence.transfer_passes}
