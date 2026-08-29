from studycheck.product_api import create_content,content_summary

def test_product_flow(tmp_path):
    source=tmp_path/'lesson.txt'; source.write_text('# 分数加法\n分母相同的分数可以直接相加',encoding='utf-8')
    content=create_content(source,'数学')
    summary=content_summary(content)
    assert summary['title']=='数学'
    assert summary['text_length']>0
    assert summary['knowledge_points']
