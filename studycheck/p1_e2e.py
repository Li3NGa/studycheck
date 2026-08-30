from __future__ import annotations
from pathlib import Path
from .file_ingest import ingest_text
from .learning_pipeline import extract_knowledge,build_practice,Progress,grade_answer
from .review_scheduler import ReviewState,record_review,due_reviews

def run_learning(path:str|Path,max_bytes:int=5_000_000)->dict:
    doc=ingest_text(path,max_bytes)
    points=extract_knowledge(doc.text)
    practice=build_practice(points)
    progress={p.id:Progress() for p in points}
    reviews={p.id:ReviewState(p.id,doc_due_at()) for p in points}
    return {'document':doc.name,'media_type':doc.media_type,'knowledge_points':[p.__dict__ for p in points],'practice':[p.__dict__ for p in practice],'progress':progress,'reviews':reviews}

def doc_due_at():
    from datetime import datetime,timezone
    return datetime.now(timezone.utc)

def submit_answer(progress:Progress,answer:str,expected:str,review:ReviewState)->dict:
    result=grade_answer(progress,answer,expected)
    record_review(review,result['correct'])
    result['next_review_at']=review.due_at.isoformat()
    result['interval_days']=review.interval_days
    result['repetitions']=review.repetitions
    result['mastery']=progress.mastery.value
    return result

def due_review_ids(reviews:list[ReviewState],limit:int=20)->list[str]:
    return [item.knowledge_id for item in due_reviews(reviews,limit=limit)]
