from __future__ import annotations
from .models import LearningEvidence,Mastery,WrongQuestion
def record_attempt(evidence:LearningEvidence,correct:bool,transfer:bool=False)->LearningEvidence:
    evidence.attempts+=1
    if correct:evidence.correct_attempts+=1
    if transfer:evidence.transfer_passes+=1
    if evidence.transfer_passes>=2 and evidence.accuracy>=0.8:evidence.mastery=Mastery.CONFIRMED
    elif evidence.attempts>=1 and evidence.accuracy<0.7:evidence.mastery=Mastery.WEAK
    else:evidence.mastery=Mastery.PRACTICED
    return evidence
def diagnose_wrong_question(question:WrongQuestion)->dict:return {"question_id":question.question_id,"subject":question.subject,"knowledge_points":question.knowledge_points,"error_type":question.error_type or "needs_ai_diagnosis","next_action":"explain_then_generate_transfer_question"}
