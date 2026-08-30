from pathlib import Path
from studycheck.learning_pipeline import learning_cycle_from_file
from studycheck.file_ingest import ingest_text, IngestError

def test_learning_cycle_from_txt(tmp_path: Path):
    p=tmp_path/'lesson.txt'; p.write_text('1. 光合作用是植物制造有机物的过程\n2. 细胞需要能量',encoding='utf-8')
    result=learning_cycle_from_file(p)
    assert result['total']==2
    assert result['knowledge_points'][0]['source']
    assert result['practice'][0]['knowledge_id']=='K0001'

def test_ingest_rejects_unsupported(tmp_path: Path):
    p=tmp_path/'lesson.md'; p.write_text('hello',encoding='utf-8')
    try: ingest_text(p)
    except IngestError as exc: assert 'unsupported' in str(exc)
    else: raise AssertionError('expected IngestError')
