from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Plan:
    name:str
    daily_reviews:int
    ai_explanations:bool
    advanced_analytics:bool

FREE=Plan('free',20,False,False)
PRO=Plan('pro',200,True,True)
FAMILY=Plan('family',500,True,True)
