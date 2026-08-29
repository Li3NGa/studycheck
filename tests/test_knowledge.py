from datetime import datetime,timezone
from studycheck.knowledge import KnowledgeGraph
from studycheck.models import Mastery

def test_due_tasks_prioritize_weak_points():
    g=KnowledgeGraph(); weak=g.add("分数加法"); weak.mastery=Mastery.WEAK
    confirmed=g.add("整数加法"); confirmed.mastery=Mastery.CONFIRMED
    g.link("分数加法","整数加法")
    tasks=g.due_tasks(datetime(2026,1,1,tzinfo=timezone.utc))
    assert tasks[0].knowledge_point=="分数加法"
    assert tasks[0].priority>tasks[1].priority
