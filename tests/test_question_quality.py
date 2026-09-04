import pytest
from studycheck.ai_provider import GeneratedQuestion
from studycheck.question_quality import assess_question

def test_quality_accepts_grounded_short_answer():
    item=GeneratedQuestion('K1','解释光合作用','植物利用光能制造有机物','答案依据资料','光合作用是植物利用光能制造有机物的过程')
    decision=assess_question(item)
    assert decision.accepted is True and decision.difficulty==3

def test_quality_rejects_invalid_type():
    item=GeneratedQuestion('K1','题目','答案','解析','来源资料')
    decision=assess_question(item,'essay',3)
    assert decision.accepted is False

def test_quality_rejects_bad_difficulty():
    item=GeneratedQuestion('K1','题目','答案','解析','来源资料')
    decision=assess_question(item,'short_answer',6)
    assert decision.accepted is False and decision.difficulty==3
