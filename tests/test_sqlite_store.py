from studycheck.sqlite_store import SQLiteLearnerRepository
from studycheck.user_state import LearnerState

def test_sqlite_round_trip(tmp_path):
    repo=SQLiteLearnerRepository(tmp_path/'test.db')
    state=LearnerState('u1'); state.session_count=3; state.total_reviews=12
    repo.save(state); loaded=repo.get('u1')
    assert loaded is not None and loaded.session_count==3 and loaded.total_reviews==12
