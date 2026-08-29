from __future__ import annotations
from datetime import datetime,timezone,timedelta
import hashlib
import secrets
from .knowledge import KnowledgeGraph
from .learning_update import apply_review
from .review_queue import build_daily_queue

def start_session(graph: KnowledgeGraph, now: datetime | None = None, limit: int = 20) -> list[dict]:
    return build_daily_queue(graph, now, limit)

def finish_review(graph: KnowledgeGraph, knowledge_point: str, correct: bool, transfer: bool = False) -> dict:
    evidence=graph.add(knowledge_point)
    apply_review(evidence, correct, transfer)
    return {"knowledge_point":knowledge_point,"mastery":evidence.mastery.value,"accuracy":evidence.accuracy,"attempts":evidence.attempts,"transfer_passes":evidence.transfer_passes}

class AuthSessionStore:
    def __init__(self,ttl_hours:int=24):
        if ttl_hours<=0: raise ValueError('ttl_hours must be positive')
        self.ttl=timedelta(hours=ttl_hours); self._items={}
    def create(self,user_id:str,tenant_id:str)->str:
        token=secrets.token_urlsafe(32)
        self._items[hashlib.sha256(token.encode()).hexdigest()] = (user_id,tenant_id,datetime.now(timezone.utc)+self.ttl)
        return token
    def get(self,token:str):
        item=self._items.get(hashlib.sha256(token.encode()).hexdigest())
        if item is None:return None
        if item[2] <= datetime.now(timezone.utc):
            self._items.pop(hashlib.sha256(token.encode()).hexdigest(),None); return None
        return {"user_id":item[0],"tenant_id":item[1],"expires_at":item[2]}
    def revoke(self,token:str)->None:
        self._items.pop(hashlib.sha256(token.encode()).hexdigest(),None)
