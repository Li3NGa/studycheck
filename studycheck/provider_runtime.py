from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from .ai_provider import GeneratedQuestion,StudyAIProvider

@dataclass(frozen=True)
class ProviderPolicy:
    timeout_seconds:float=30.0
    max_attempts:int=2

class ProviderRuntime:
    def __init__(self,provider:StudyAIProvider,policy:ProviderPolicy|None=None): self.provider=provider; self.policy=policy or ProviderPolicy()
    def generate(self,knowledge_id:str,title:str,source:str)->GeneratedQuestion:
        if self.policy.timeout_seconds<=0 or self.policy.max_attempts<1: raise ValueError('invalid provider policy')
        started=monotonic(); last=None
        for _ in range(self.policy.max_attempts):
            try:
                result=self.provider.generate(knowledge_id,title,source)
                if monotonic()-started>self.policy.timeout_seconds: raise TimeoutError('provider timeout')
                if not result.source.strip(): raise ValueError('generated item must retain source')
                return result
            except Exception as exc: last=exc
        raise RuntimeError('provider failed') from last
