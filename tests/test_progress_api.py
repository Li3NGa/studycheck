from studycheck.api import StudyCheckService
from studycheck.http_api import progress
from studycheck.store import MemoryLearnerRepository

def test_progress_reports_persisted_learner_metrics():
    service=StudyCheckService(MemoryLearnerRepository())
    result=progress(service,'u1')
    assert result['user_id']=='u1'
    assert result['session_count']==0
    assert result['total_reviews']==0
    assert result['knowledge_points']==0
