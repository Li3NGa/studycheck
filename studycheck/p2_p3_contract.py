from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable

@dataclass(frozen=True)
class LearningTask:
    task_id:str; user_id:str; status:str='queued'; error:str|None=None

@dataclass(frozen=True)
class APIResult:
    status:int; data:dict[str,Any]

def run_learning_task(user_id:str,runner:Callable[[str],dict[str,Any]])->APIResult:
    if not user_id.strip(): return APIResult(400,{'error':'invalid_user_id'})
    try: result=runner(user_id); return APIResult(200,{'status':'completed','result':result})
    except Exception: return APIResult(500,{'error':'learning_failed'})
