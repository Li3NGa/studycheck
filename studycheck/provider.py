from __future__ import annotations
from typing import Protocol, Any

class AIProvider(Protocol):
    def generate(self, payload: dict[str, Any]) -> dict[str, Any]: ...

class ProviderError(RuntimeError): pass

def generate(provider: AIProvider, payload: dict[str, Any]) -> dict[str, Any]:
    result=provider.generate(payload)
    if not isinstance(result,dict): raise ProviderError("AI provider must return an object")
    return result
