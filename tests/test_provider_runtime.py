from studycheck.ai_provider import GeneratedQuestion
from studycheck.provider_runtime import ProviderPolicy,ProviderRuntime

class Provider:
    def generate(self,knowledge_id,title,source):
        return GeneratedQuestion(knowledge_id,title,source,'依据原资料',source)

def test_usage_and_cost():
    runtime=ProviderRuntime(Provider(),ProviderPolicy(cost_per_call=0.01))
    result=runtime.generate('K1','标题','资料')
    assert result.source=='资料'
    assert runtime.usage.calls==1
    assert runtime.usage.estimated_cost==0.01
