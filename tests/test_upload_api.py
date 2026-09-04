import base64
from pathlib import Path
from studycheck.api import StudyCheckService
from studycheck.store import MemoryLearnerRepository
from studycheck.upload_api import ingest_uploaded_material

def enc(text:str)->str:return base64.b64encode(text.encode()).decode()

def test_upload_material_creates_learning_result(tmp_path:Path):
    service=StudyCheckService(MemoryLearnerRepository())
    payload={'user_id':'u1','filename':'lesson.txt','content_base64':enc('1. 光合作用利用光能制造有机物\n2. 细胞是生命的基本单位')}
    result=ingest_uploaded_material(service,payload,tmp_path)
    assert result['user_id']=='u1'
    assert result['total']==2
    assert result['content_id']
