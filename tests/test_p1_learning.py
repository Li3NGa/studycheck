from datetime import datetime,timezone
from studycheck.learning_pipeline import extract_knowledge,build_practice,Progress,grade_answer
from studycheck.review_scheduler import ReviewState,record_review,due_reviews

def test_learning_loop():
    points=extract_knowledge('1、光合作用是植物制造有机物的过程\n2、细胞是生物体结构和功能的基本单位')
    assert len(points)==2
    practice=build_practice(points); progress=Progress()
    result=grade_answer(progress,practice[0].answer,practice[0].answer)
    assert result['correct'] is True
    assert result['accuracy']==1.0

def test_review_schedule():
    now=datetime(2026,1,1,tzinfo=timezone.utc); state=ReviewState('K0001',now)
    record_review(state,True,now)
    assert state.due_at>now
    assert due_reviews([state],now)==[]
