from __future__ import annotations
from .user_state import LearnerState
from .serialization import graph_to_dict,graph_from_dict

def state_to_dict(state:LearnerState)->dict:
    return {"user_id":state.user_id,"graph":graph_to_dict(state.graph),"session_count":state.session_count,"total_reviews":state.total_reviews}

def state_from_dict(data:dict)->LearnerState:
    state=LearnerState(str(data["user_id"]),graph_from_dict(data.get("graph",{})))
    state.session_count=int(data.get("session_count",0)); state.total_reviews=int(data.get("total_reviews",0))
    return state
