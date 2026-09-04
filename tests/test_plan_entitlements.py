import pytest
from studycheck.api import StudyCheckService
from studycheck.entitlements import plan_entitlements,require_feature
from studycheck.plans import FREE,PRO
from studycheck.store import MemoryLearnerRepository

def test_free_entitlements_report_remaining_usage():
    service=StudyCheckService(MemoryLearnerRepository())
    service.usage.consume_review()
    result=plan_entitlements(service.plan,service.usage)
    assert result['plan']=='free'
    assert result['reviews_used']==1
    assert result['reviews_remaining']==19

def test_free_plan_blocks_paid_feature():
    with pytest.raises(PermissionError): require_feature(FREE,'ai_explanations')
    require_feature(PRO,'ai_explanations')
