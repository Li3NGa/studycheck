from pathlib import Path
from studycheck.product_api import ingest_material, review_answer
from studycheck.api import StudyCheckService
from studycheck.store import MemoryLearnerRepository

def test_material_and_review_flow(tmp_path: Path):
    p=tmp_path/'lesson.txt'; p.write_text('光合作用需要光能。植物制造有机物。',encoding='utf-8')
    service=StudyCheckService(MemoryLearnerRepository())
    result=ingest_material(service,'u1',p)
    assert result['user_id']=='u1'
    assert result['content_id']
    assert result['total']>=1
    point=result['knowledge_points'][0]['id']
    review=review_answer(service,'u1',point,True)
    assert review['knowledge_id']==point
