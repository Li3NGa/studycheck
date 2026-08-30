from datetime import datetime, timedelta, timezone
from studycheck.review_scheduler import ReviewState, record_review, due_reviews

def test_correct_review_increases_interval():
    now=datetime(2026,1,1,tzinfo=timezone.utc)
    s=ReviewState('K1',now)
    record_review(s,True,now)
    assert s.repetitions==1 and s.interval_days==2 and s.due_at==now+timedelta(days=2)

def test_wrong_review_resets_interval():
    now=datetime(2026,1,5,tzinfo=timezone.utc)
    s=ReviewState('K1',now,interval_days=8,repetitions=4)
    record_review(s,False,now)
    assert s.repetitions==0 and s.interval_days==1 and s.due_at==now+timedelta(days=1)

def test_due_reviews_sorted_and_limited():
    now=datetime(2026,1,10,tzinfo=timezone.utc)
    states=[ReviewState('late',now-timedelta(days=2)),ReviewState('early',now-timedelta(days=3)),ReviewState('future',now+timedelta(days=1))]
    assert [s.knowledge_id for s in due_reviews(states,now,limit=1)]==['early']
