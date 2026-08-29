from studycheck.ocr import extract_question
from studycheck.provider import generate
class FakeOCR:
    def extract_text(self,b): return "题目：2+2=?"
class FakeAI:
    def generate(self,p): return {"question":"3+3=?","answer":"6"}
def test_ocr_contract(): assert extract_question(FakeOCR(),b"x").text.startswith("题目")
def test_provider_contract(): assert generate(FakeAI(),{"task":"x"})["answer"]=="6"
