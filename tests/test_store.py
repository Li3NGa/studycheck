from studycheck.store import MemoryLearnerRepository
from studycheck.user_state import LearnerState

def test_learner_repository_round_trip():
    repo=MemoryLearnerRepository(); state=LearnerState('u1'); repo.save(state)
    assert repo.get('u1') is state
    assert repo.get('missing') is None
