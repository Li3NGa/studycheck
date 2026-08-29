from __future__ import annotations
from .auth_middleware import authenticate_bearer
from .session import AuthSessionStore
from .content_models import LearningContent
from .tenant_guard import require_content_access

def authorize_content(authorization:str,content:LearningContent,sessions:AuthSessionStore)->LearningContent:
    user=authenticate_bearer(authorization,sessions)
    require_content_access(content,user)
    return content
