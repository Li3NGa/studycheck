from __future__ import annotations

def quality_gate(result: dict, expected_subject: str, expected_points: list[str]) -> dict:
    required=("question","answer","explanation","knowledge_points")
    missing=[k for k in required if k not in result]
    if missing: return {"passed":False,"reasons":[f"missing:{k}" for k in missing]}
    reasons=[]
    if not all(isinstance(result[k],str) and result[k].strip() for k in ("question","answer","explanation")): reasons.append("empty_text")
    if not isinstance(result["knowledge_points"],list): reasons.append("invalid_knowledge_points")
    overlap=set(expected_points)&set(result["knowledge_points"]) if isinstance(result["knowledge_points"],list) else set()
    if expected_points and not overlap: reasons.append("knowledge_point_mismatch")
    return {"passed":not reasons,"reasons":reasons,"knowledge_overlap":sorted(overlap)}
