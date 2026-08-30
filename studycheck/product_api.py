from __future__ import annotations
from pathlib import Path
from .content_workflow import ingest_content
from .api import StudyCheckService
from .learning_pipeline import learning_cycle_from_file

def create_content(path:str|Path,title:str|None=None):
    return ingest_content(path,title)

def content_summary(content)->dict:
    return {'content_id':content.content_id,'title':content.title,'knowledge_points':content.knowledge_points,'text_length':len(content.text)}

def ingest_material(service: StudyCheckService, user_id: str, path: str | Path) -> dict:
    if not user_id or not user_id.strip():
        raise ValueError('user_id is required')
    result = learning_cycle_from_file(path)
    state = service.get_or_create(user_id)
    if hasattr(state, 'total_knowledge'):
        state.total_knowledge = max(state.total_knowledge, result['total'])
    service.repository.save(state)
    result['user_id'] = user_id
    return result

def review_answer(service: StudyCheckService, user_id: str, knowledge_point: str, correct: bool, transfer: bool = False) -> dict:
    return service.review(user_id, knowledge_point, correct, transfer)
