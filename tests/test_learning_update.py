from studycheck.learning_update import apply_review
from studycheck.models import LearningEvidence,Mastery

def test_failed_review_keeps_point_weak():
    e=LearningEvidence('分数',Mastery.PRACTICED,2,1,0)
    apply_review(e,False)
    assert e.mastery==Mastery.WEAK

def test_two_transfer_passes_confirm_mastery():
    e=LearningEvidence('整数加法',Mastery.PRACTICED,2,2,1)
    apply_review(e,True,True)
    assert e.mastery==Mastery.CONFIRMED
