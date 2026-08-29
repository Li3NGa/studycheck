from datetime import datetime,timezone
from studycheck.mastery import schedule_review
from studycheck.models import LearningEvidence,Mastery

def test_weak_is_urgent():
    e=LearningEvidence("分数",Mastery.WEAK,3,1,0)
    task=schedule_review(e,datetime(2026,1,1,tzinfo=timezone.utc))
    assert task.priority==100 and task.due_at.day==2

def test_confirmed_is_spaced():
    e=LearningEvidence("分数",Mastery.CONFIRMED,10,9,2)
    task=schedule_review(e,datetime(2026,1,1,tzinfo=timezone.utc))
    assert task.priority==20 and task.due_at.day==15
