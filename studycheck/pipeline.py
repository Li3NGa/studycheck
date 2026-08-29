from __future__ import annotations
from .diagnosis import build_diagnosis_prompt
from .intake import intake
from .ocr import extract_question
from .provider import generate
from .quality import quality_gate
from .variation import build_variation_prompt

def process_image(provider, ocr_provider, image_bytes: bytes, subject: str, user_answer: str, correct_answer: str, knowledge_points: list[str] | None = None) -> dict:
    ocr=extract_question(ocr_provider, image_bytes)
    question=intake(subject, ocr.text, user_answer, correct_answer, knowledge_points)
    diagnosis=generate(provider, build_diagnosis_prompt(question))
    question.error_type=diagnosis.get("error_type")
    variation=generate(provider, build_variation_prompt(question))
    gate=quality_gate(variation, subject, question.knowledge_points)
    return {"question":question,"diagnosis":diagnosis,"variation":variation,"quality":gate}
