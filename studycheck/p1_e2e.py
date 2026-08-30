from __future__ import annotations
from .file_ingest import ingest_text
from .learning_pipeline import extract_knowledge,build_practice,Progress,grade_answer
from .review_scheduler import ReviewState,record_review

def run_learning(path:str)->dict:
    doc=ingest_text(path); points=extract_knowledge(doc.text); practice=build_practice(points)
    progress={p.id:Progress() for p in points}
    return {'document':doc.name,'knowledge_points':[p.__dict__ for p in points],'practice':[p.__dict__ for p in practice],'progress':progress}

def submit_answer(progress:Progress,answer:str,expected:str,review:ReviewState)->dict:
    result=grade_answer(progress,answer,expected); record_review(review,result['correct']); result['next_review_at']=review.due_at.isoformat(); return result
