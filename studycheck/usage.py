from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Usage:
    user_id:str
    generations:int=0
    submissions:int=0

class UsageLimitError(PermissionError): pass

def consume_generation(usage:Usage,limit:int)->Usage:
    if usage.generations>=limit: raise UsageLimitError('generation quota exceeded')
    usage.generations+=1
    return usage
