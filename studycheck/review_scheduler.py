from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone

@dataclass
class ReviewState:
    knowledge_id:str; due_at:datetime; interval_days:int=1; repetitions:int=0

def record_review(state:ReviewState,correct:bool,now:datetime|None=None)->ReviewState:
    now=now or datetime.now(timezone.utc)
    if correct:
        state.repetitions+=1
        state.interval_days=min(30,max(1,state.interval_days*2))
    else:
        state.repetitions=0; state.interval_days=1
    state.due_at=now+timedelta(days=state.interval_days)
    return state

def due_reviews(states:list[ReviewState],now:datetime|None=None,limit:int=20)->list[ReviewState]:
    now=now or datetime.now(timezone.utc)
    if limit<1: raise ValueError('limit must be positive')
    return sorted((s for s in states if s.due_at<=now),key=lambda s:s.due_at)[:limit]
