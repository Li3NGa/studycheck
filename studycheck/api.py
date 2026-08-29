from __future__ import annotations
from .review_queue import build_daily_queue
from .session import finish_review
from .store import LearnerRepository
from .user_state import LearnerState

class StudyCheckService:
    def __init__(self, repository: LearnerRepository): self.repository=repository
    def get_or_create(self,user_id:str)->LearnerState:
        state=self.repository.get(user_id)
        if state is None:
            state=LearnerState(user_id); self.repository.save(state)
        return state
    def daily_queue(self,user_id:str,limit:int=20)->list[dict]:
        return build_daily_queue(self.get_or_create(user_id).graph,limit=limit)
    def review(self,user_id:str,knowledge_point:str,correct:bool,transfer:bool=False)->dict:
        state=self.get_or_create(user_id)
        result=finish_review(state.graph,knowledge_point,correct,transfer)
        state.total_reviews+=1
        self.repository.save(state)
        return result
