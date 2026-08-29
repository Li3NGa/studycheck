import pytest
from studycheck.api import StudyCheckService
from studycheck.http_api import APIError,daily_queue,review
from studycheck.store import MemoryLearnerRepository

def test_queue_validates_limit():
    with pytest.raises(APIError) as exc: daily_queue(StudyCheckService(MemoryLearnerRepository()),'u1',0)
    assert exc.value.status==400

def test_review_requires_boolean_correct():
    with pytest.raises(APIError) as exc: review(StudyCheckService(MemoryLearnerRepository()),{'user_id':'u1','knowledge_point':'分数','correct':'false'})
    assert exc.value.code=='invalid_review'
