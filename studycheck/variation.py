from __future__ import annotations
from .models import WrongQuestion

def build_variation_prompt(question:WrongQuestion)->dict:
    return {"task":"generate_transfer_question","constraints":["Test the same knowledge point with a meaningfully different surface form.","Do not reveal the answer in the question.","Return one question, answer, explanation and knowledge points.","Preserve subject and approximate difficulty."],"input":{"subject":question.subject,"original_question":question.content,"knowledge_points":question.knowledge_points,"error_type":question.error_type or "unknown"},"output_schema":{"question":"string","answer":"string","explanation":"string","knowledge_points":["string"]}}
