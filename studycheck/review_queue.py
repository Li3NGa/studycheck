from __future__ import annotations
from datetime import datetime
from .knowledge import KnowledgeGraph

def build_daily_queue(graph: KnowledgeGraph, now: datetime | None = None, limit: int = 20) -> list[dict]:
    tasks=graph.due_tasks(now)
    return [{"knowledge_point":t.knowledge_point,"due_at":t.due_at.isoformat(),"priority":t.priority} for t in tasks[:max(0,limit)]]
