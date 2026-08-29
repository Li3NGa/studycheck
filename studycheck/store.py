from __future__ import annotations
from dataclasses import dataclass
from .user_state import LearnerState

class LearnerRepository:
    def save(self, state: LearnerState) -> None: raise NotImplementedError
    def get(self, user_id: str) -> LearnerState | None: raise NotImplementedError

@dataclass
class MemoryLearnerRepository(LearnerRepository):
    states: dict[str,LearnerState]
    def __init__(self): self.states={}
    def save(self,state:LearnerState)->None: self.states[state.user_id]=state
    def get(self,user_id:str)->LearnerState|None: return self.states.get(user_id)
