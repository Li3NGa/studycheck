from __future__ import annotations
from .models import LearningEvidence,Mastery

def apply_review(evidence: LearningEvidence, correct: bool, transfer: bool=False) -> LearningEvidence:
    evidence.attempts += 1
    if correct: evidence.correct_attempts += 1
    if transfer: evidence.transfer_passes += 1
    if evidence.transfer_passes >= 2 and evidence.accuracy >= 0.8:
        evidence.mastery=Mastery.CONFIRMED
    elif evidence.accuracy < 0.7:
        evidence.mastery=Mastery.WEAK
    else:
        evidence.mastery=Mastery.PRACTICED
    return evidence
