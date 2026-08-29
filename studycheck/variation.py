from __future__ import annotations
from .models import WrongQuestion

def build_variation_prompt(question: WrongQuestion) -> dict:
    return {"task":"generate_transfer_question","constraints":["Test the same knowledge point with a meaningfully different surface form.","Do not reveal the answer.","Return question, answer, explanation and knowledge points.","Preserve subject and approximate difficulty."],"input":{"subject":question.subject,"original_question":question.content,"knowledge_points":question.knowledge_points,"error_type":question.error_type or "unknown"},"output_schema":{"question":"string","answer":"string","explanation":"string","knowledge_points":["string"]}}

def validate_variation(result: dict, subject: str, knowledge_points: list[str]) -> dict:
    required={"question","answer","explanation","knowledge_points"}
    missing=required-set(result)
    if missing: raise ValueError(f"variation missing fields: {sorted(missing)}")
    if not str(result["question"]).strip() or not str(result["answer"]).strip(): raise ValueError("empty generated question or answer")
    if not isinstance(result["knowledge_points"],list): raise ValueError("knowledge_points must be a list")
    overlap=set(knowledge_points)&set(result["knowledge_points"])
    return {"valid":True,"subject":subject,"knowledge_overlap":sorted(overlap),"result":result}
