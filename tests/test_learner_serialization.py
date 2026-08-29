from studycheck.learner_serialization import state_to_dict,state_from_dict
from studycheck.user_state import LearnerState

def test_state_round_trip():
    s=LearnerState('u1'); e=s.graph.add('分数'); e.attempts=4; e.correct_attempts=3; s.graph.link('分数','小数'); s.session_count=2; s.total_reviews=4
    q=state_from_dict(state_to_dict(s))
    assert q.user_id=='u1' and q.graph.evidence['分数'].attempts==4 and '小数' in q.graph.edges['分数'] and q.total_reviews==4
