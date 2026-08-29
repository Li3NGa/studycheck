from __future__ import annotations
from dataclasses import dataclass,field
from .knowledge import KnowledgeGraph

@dataclass
class LearnerState:
    user_id: str
    graph: KnowledgeGraph=field(default_factory=KnowledgeGraph)
    session_count: int=0
    total_reviews: int=0

def record_session(state:LearnerState, reviews:int)->None:
    state.session_count += 1
    state.total_reviews += max(0,reviews)
