from studycheck.knowledge import KnowledgeGraph
from studycheck.models import Mastery
from studycheck.serialization import graph_to_dict,graph_from_dict

def test_knowledge_graph_round_trip():
    g=KnowledgeGraph(); e=g.add('分数'); e.mastery=Mastery.WEAK; e.attempts=4; e.correct_attempts=2; g.link('分数','分数加法')
    loaded=graph_from_dict(graph_to_dict(g))
    assert loaded.evidence['分数'].mastery is Mastery.WEAK
    assert '分数加法' in loaded.edges['分数']
