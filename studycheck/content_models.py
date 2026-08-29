from __future__ import annotations
from dataclasses import dataclass,field
from uuid import uuid4
from .tenant import User,assert_tenant_access

@dataclass
class LearningContent:
    title:str
    text:str
    knowledge_points:list[str]=field(default_factory=list)
    content_id:str=field(default_factory=lambda:uuid4().hex)
    tenant_id:str|None=None

    def assert_access(self,user:User)->None:
        if self.tenant_id: assert_tenant_access(user,self.tenant_id)
