from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
from typing import Any
class Mastery(str,Enum): UNSEEN="unseen"; PRACTICED="practiced"; WEAK="weak"; CONFIRMED="confirmed"
@dataclass
class WrongQuestion:
    question_id:str; subject:str; content:str; user_answer:str; correct_answer:str; knowledge_points:list[str]=field(default_factory=list); error_type:str|None=None; metadata:dict[str,Any]=field(default_factory=dict)
@dataclass
class LearningEvidence:
    knowledge_point:str; mastery:Mastery=Mastery.UNSEEN; attempts:int=0; correct_attempts:int=0; transfer_passes:int=0
    @property
    def accuracy(self)->float:return self.correct_attempts/self.attempts if self.attempts else 0.0
