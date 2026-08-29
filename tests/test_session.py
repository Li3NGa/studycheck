from studycheck.knowledge import KnowledgeGraph
from studycheck.models import Mastery
from studycheck.session import start_session,finish_review

def test_session_returns_weak_point_first():
    g=KnowledgeGraph(); e=g.add('分数'); e.mastery=Mastery.WEAK
    e2=g.add('整数'); e2.mastery=Mastery.CONFIRMED
    assert start_session(g,limit=1)[0]['knowledge_point']=='分数'

def test_finish_review_updates_state():
    g=KnowledgeGraph(); result=finish_review(g,'分数',False)
    assert result['mastery']=='weak' and result['attempts']==1
