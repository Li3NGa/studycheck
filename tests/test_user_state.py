from studycheck.user_state import LearnerState,record_session

def test_record_session_updates_counters():
    state=LearnerState('u1')
    record_session(state,5)
    record_session(state,-1)
    assert state.session_count==2
    assert state.total_reviews==5
