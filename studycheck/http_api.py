from __future__ import annotations
from typing import Any
from .api import StudyCheckService
from .auth_middleware import authenticate_bearer
from .session import AuthSessionStore

class APIError(Exception):
    def __init__(self,status:int,code:str,message:str): self.status=status; self.code=code; self.message=message

def require_auth(authorization:str|None,sessions:AuthSessionStore)->dict:
    if not authorization: raise APIError(401,'authentication_required','authentication required')
    try: user=authenticate_bearer(authorization,sessions)
    except PermissionError as exc: raise APIError(401,'authentication_required',str(exc)) from exc
    return {'user_id':user.user_id,'tenant_id':user.tenant_id}

def daily_queue(service:StudyCheckService,user_id:str,limit:int=20,authorization:str|None=None,sessions:AuthSessionStore|None=None)->list[dict[str,Any]]:
    if sessions is not None:
        auth=require_auth(authorization,sessions)
        if user_id!=auth['user_id']: raise APIError(403,'forbidden','user access denied')
    if not user_id: raise APIError(400,'invalid_user','user_id is required')
    if limit<1 or limit>100: raise APIError(400,'invalid_limit','limit must be between 1 and 100')
    return service.daily_queue(user_id,limit)

def review(service:StudyCheckService,payload:dict[str,Any],authorization:str|None=None,sessions:AuthSessionStore|None=None)->dict[str,Any]:
    if not isinstance(payload,dict) or not payload.get('user_id') or not payload.get('knowledge_point') or not isinstance(payload.get('correct'),bool): raise APIError(400,'invalid_review','user_id, knowledge_point and boolean correct are required')
    if sessions is not None:
        auth=require_auth(authorization,sessions)
        if str(payload['user_id'])!=auth['user_id']: raise APIError(403,'forbidden','user access denied')
    return service.review(str(payload['user_id']),str(payload['knowledge_point']),payload['correct'],bool(payload.get('transfer',False)))
