from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .models import WrongQuestion
class ErrorType(str,Enum): CONCEPT="concept"; CALCULATION="calculation"; READING="reading"; METHOD="method"; CARELESS="careless"; KNOWLEDGE_GAP="knowledge_gap"; UNKNOWN="unknown"
@dataclass(frozen=True)
class Diagnosis:error_type:ErrorType; reason:str; evidence:list[str]; confidence:float
def build_diagnosis_prompt(question:WrongQuestion)->dict:return {"task":"diagnose_wrong_answer","constraints":["Only infer from supplied question, answer and reference answer.","Do not invent missing facts.","Return one primary error type and evidence.","Use low confidence when evidence is insufficient."],"input":{"subject":question.subject,"question":question.content,"student_answer":question.user_answer,"reference_answer":question.correct_answer,"knowledge_points":question.knowledge_points},"output_schema":{"error_type":"concept|calculation|reading|method|careless|knowledge_gap|unknown","reason":"string","evidence":["string"],"confidence":"0..1"}}
