from __future__ import annotations
from dataclasses import dataclass,field
from uuid import uuid4

@dataclass
class LearningContent:
    title:str
    text:str
    knowledge_points:list[str]=field(default_factory=list)
    content_id:str=field(default_factory=lambda:uuid4().hex)
