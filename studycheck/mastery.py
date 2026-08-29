from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from .models import LearningEvidence,Mastery
@dataclass(frozen=True)
class ReviewTask:
    knowledge_point:str
    due_at:datetime
    priority:int

def schedule_review(evidence:LearningEvidence, now:datetime|None=None)->ReviewTask:
    now=now or datetime.now(timezone.utc)
    if evidence.attempts>=5 and evidence.accuracy<0.5: days,priority=0,120
    elif evidence.mastery is Mastery.WEAK: days,priority=1,100
    elif evidence.mastery is Mastery.PRACTICED: days,priority=3,60
    elif evidence.mastery is Mastery.CONFIRMED: days,priority=14,20
    else: days,priority=0,80
    return ReviewTask(evidence.knowledge_point,now+timedelta(days=days),priority)
