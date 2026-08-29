from __future__ import annotations
import json,sqlite3
from pathlib import Path
from .learner_serialization import state_to_dict,state_from_dict
from .user_state import LearnerState

class SQLiteLearnerRepository:
    def __init__(self,path:str|Path='studycheck.db'):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS learners (user_id TEXT PRIMARY KEY, payload TEXT NOT NULL)'); db.commit()
    def save(self,state:LearnerState)->None:
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO learners(user_id,payload) VALUES(?,?)',(state.user_id,json.dumps(state_to_dict(state),ensure_ascii=False))); db.commit()
    def get(self,user_id:str)->LearnerState|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT payload FROM learners WHERE user_id=?',(user_id,)).fetchone()
        return state_from_dict(json.loads(row[0])) if row else None
