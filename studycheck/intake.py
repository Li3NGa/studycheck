from __future__ import annotations
import hashlib
from .models import WrongQuestion
def make_question_id(content:str,subject:str)->str:return hashlib.sha256(f"{subject}\n{content}".encode()).hexdigest()[:16]
def intake(subject:str,content:str,user_answer:str,correct_answer:str,knowledge_points:list[str]|None=None)->WrongQuestion:return WrongQuestion(make_question_id(content,subject),subject,content,user_answer,correct_answer,knowledge_points or [])
