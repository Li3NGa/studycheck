import pytest
from studycheck.ai_provider import DeterministicProvider, GeneratedQuestion, generate_questions, validate_generated
from studycheck.learning_pipeline import extract_knowledge

def test_generate_questions_retains_source():
    points=extract_knowledge('光合作用是植物制造有机物的过程。')
    result=generate_questions(points,DeterministicProvider())
    assert len(result)==1
    assert result[0].knowledge_id==points[0].id
    assert result[0].source==points[0].source

def test_validate_generated_rejects_missing_source():
    item=GeneratedQuestion('K1','题目','答案','解析','')
    with pytest.raises(ValueError): validate_generated(item)
