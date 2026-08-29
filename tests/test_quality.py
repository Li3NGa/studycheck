from studycheck.quality import quality_gate

def test_quality_gate_accepts_valid_transfer():
    result={"question":"3+3=?","answer":"6","explanation":"加法","knowledge_points":["整数加法"]}
    assert quality_gate(result,"数学",["整数加法"])["passed"]

def test_quality_gate_rejects_wrong_knowledge_point():
    result={"question":"x","answer":"1","explanation":"y","knowledge_points":["分数"]}
    assert not quality_gate(result,"数学",["整数加法"])["passed"]
