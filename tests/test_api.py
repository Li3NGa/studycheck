from studycheck.api import StudyCheckService
from studycheck.models import Mastery
from studycheck.store import MemoryLearnerRepository

def test_daily_queue_and_review():
    service=StudyCheckService(MemoryLearnerRepository())
    state=service.get_or_create('u1'); state.graph.add('分数').mastery=Mastery.WEAK
    q=service.daily_queue('u1',1)
    assert q[0]['knowledge_point']=='分数'
    result=service.review('u1','分数',False)
    assert result['mastery']=='weak'
