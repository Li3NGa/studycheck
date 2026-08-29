from studycheck.content_pipeline import extract_knowledge_points

def test_extract_points(tmp_path):
    p=tmp_path/'lesson.txt'; p.write_text('# 分数的加法\n分母相同的分数可以直接相加\n\n1. x',encoding='utf-8')
    points=extract_knowledge_points(p)
    assert '分数的加法' in points
