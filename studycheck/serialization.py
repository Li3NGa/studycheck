from __future__ import annotations
from .knowledge import KnowledgeGraph
from .models import LearningEvidence,Mastery

def graph_to_dict(graph:KnowledgeGraph)->dict:
    return {"evidence":{k:{"knowledge_point":v.knowledge_point,"mastery":v.mastery.value,"attempts":v.attempts,"correct_attempts":v.correct_attempts,"transfer_passes":v.transfer_passes} for k,v in graph.evidence.items()},"edges":{k:sorted(v) for k,v in graph.edges.items()}}

def graph_from_dict(data:dict)->KnowledgeGraph:
    if not isinstance(data,dict): raise ValueError('invalid knowledge graph')
    graph=KnowledgeGraph()
    for point,item in data.get('evidence',{}).items():
        e=LearningEvidence(str(point)); e.mastery=Mastery(item.get('mastery',Mastery.PRACTICED.value)); e.attempts=int(item.get('attempts',0)); e.correct_attempts=int(item.get('correct_attempts',0)); e.transfer_passes=int(item.get('transfer_passes',0)); graph.evidence[str(point)]=e
    for source,targets in data.get('edges',{}).items():
        for target in targets: graph.link(str(source),str(target))
    return graph
