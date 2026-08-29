from __future__ import annotations
from dataclasses import dataclass,field
from .mastery import ReviewTask,schedule_review
from .models import LearningEvidence

@dataclass
class KnowledgeGraph:
    evidence: dict[str,LearningEvidence]=field(default_factory=dict)
    edges: dict[str,set[str]]=field(default_factory=dict)
    def add(self, point:str)->LearningEvidence:
        return self.evidence.setdefault(point,LearningEvidence(point))
    def link(self, source:str, target:str)->None:
        self.add(source); self.add(target); self.edges.setdefault(source,set()).add(target)
    def due_tasks(self, now=None)->list[ReviewTask]:
        return sorted((schedule_review(e,now) for e in self.evidence.values()),key=lambda t:(-t.priority,t.due_at))
