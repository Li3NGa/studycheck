from __future__ import annotations
from .tenant import User
from .content_models import LearningContent

def require_content_access(content:LearningContent,user:User)->None:
    if content.tenant_id is None:
        raise PermissionError('content has no tenant owner')
    if user.tenant_id != content.tenant_id:
        raise PermissionError('tenant access denied')
