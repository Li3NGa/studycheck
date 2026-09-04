from __future__ import annotations
from pathlib import Path
from typing import Any
import base64,binascii
from .api import StudyCheckService
from .product_api import ingest_material
from .upload import save_upload,UploadError
from .http_api import APIError

def _save(payload:dict[str,Any],directory:str|Path,max_bytes:int)->str:
    if not isinstance(payload,dict) or not payload.get('filename') or not payload.get('content_base64'):
        raise APIError(400,'invalid_material','filename and content_base64 are required')
    try:data=base64.b64decode(str(payload['content_base64']),validate=True)
    except (binascii.Error,ValueError) as exc:raise APIError(400,'invalid_base64','content_base64 is invalid') from exc
    try:return save_upload(data,str(payload['filename']),directory,max_bytes)
    except UploadError as exc:raise APIError(400,'invalid_material',str(exc)) from exc

def ingest_uploaded_material(service:StudyCheckService,payload:dict[str,Any],directory:str|Path='uploads',max_bytes:int=10_000_000)->dict:
    if not isinstance(payload,dict) or not payload.get('user_id'):
        raise APIError(400,'invalid_user','user_id is required')
    path=_save(payload,directory,max_bytes)
    return ingest_material(service,str(payload['user_id']),path)
