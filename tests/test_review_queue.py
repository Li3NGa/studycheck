from studycheck.knowledge import KnowledgeGraph
from studycheck.models import Mastery
from studycheck.review_queue import build_daily_queue

def test_queue_is_priority_ordered_and_limited():
    g=KnowledgeGraph()
    for i in range(3):
        e=g.add(f'知识点{i}'); e.mastery=Mastery.WEAK
    q=build_daily_queue(g,limit=2)
    assert len(q)==2
    assert q[0]['priority']==100
