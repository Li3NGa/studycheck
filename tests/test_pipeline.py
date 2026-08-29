from studycheck.pipeline import process_image

class OCR:
    def extract_text(self, image_bytes):
        assert image_bytes == b'image'
        return '2+2=?'

class AI:
    def __init__(self): self.calls=0
    def generate(self, payload):
        self.calls += 1
        if payload['task']=='diagnose_wrong_answer': return {'error_type':'calculation','reason':'计算错误','evidence':['student_answer'], 'confidence':0.95}
        return {'question':'3+3=?','answer':'6','explanation':'加法','knowledge_points':['整数加法']}

def test_pipeline_connects_ocr_diagnosis_variation_and_gate():
    ai=AI(); result=process_image(ai, OCR(), b'image', '数学', '5', '4', ['整数加法'])
    assert result['question'].content == '2+2=?'
    assert result['diagnosis']['error_type'] == 'calculation'
    assert result['quality']['passed'] is True
    assert ai.calls == 2
