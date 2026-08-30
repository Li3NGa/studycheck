from studycheck.document_parser import extract_text,DocumentParseError

def test_txt(tmp_path):
    p=tmp_path/'a.txt'; p.write_text('光合作用是植物制造有机物的过程',encoding='utf-8')
    assert '光合作用' in extract_text(p)

def test_unsupported(tmp_path):
    p=tmp_path/'a.csv'; p.write_text('x',encoding='utf-8')
    try: extract_text(p)
    except DocumentParseError as exc: assert 'unsupported' in str(exc)
    else: raise AssertionError('expected error')
