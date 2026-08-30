import pytest
from studycheck.ai_provider import GeneratedQuestion
from studycheck.provider_runtime import ProviderPolicy, ProviderRuntime

class Provider:
    def generate(self, knowledge_id, title, source):
        return GeneratedQuestion(knowledge_id, title, '答案', '依据原资料', source)

def test_usage_and_cost():
    runtime = ProviderRuntime(Provider(), ProviderPolicy(cost_per_call=0.01))
    result = runtime.generate('K1', '标题', '资料')
    assert result.source == '资料'
    assert result.knowledge_id == 'K1'
    assert runtime.usage.calls == 1
    assert runtime.usage.estimated_cost == 0.01

def test_mismatched_knowledge_is_rejected():
    class BadProvider(Provider):
        def generate(self, knowledge_id, title, source):
            return GeneratedQuestion('OTHER', title, '答案', '解释', source)
    with pytest.raises(RuntimeError):
        ProviderRuntime(BadProvider(), ProviderPolicy(max_attempts=1)).generate('K1', '标题', '资料')
