from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Callable

@dataclass(frozen=True)
class EndpointResult:
    status:int; body:dict[str,Any]

def study_session(payload:dict[str,Any])->EndpointResult:
    if not isinstance(payload,dict) or not payload.get('user_id'): return EndpointResult(400,{'error':'invalid_user'})
    return EndpointResult(201,{'user_id':str(payload['user_id']),'status':'created'})

def answer_submit(user_id:str,runner:Callable[[str],dict[str,Any]])->EndpointResult:
    if not user_id: return EndpointResult(400,{'error':'invalid_user_id'})
    try:return EndpointResult(200,{'status':'completed','result':runner(user_id)})
    except Exception:return EndpointResult(500,{'error':'answer_failed'})
