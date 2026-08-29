from __future__ import annotations
import sqlite3
from pathlib import Path
from .user_state import LearnerState

class SQLiteLearnerRepository:
    def __init__(self,path:str|Path='studycheck.db'):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS learners (user_id TEXT PRIMARY KEY, session_count INTEGER NOT NULL, total_reviews INTEGER NOT NULL)')
            db.commit()
    def save(self,state:LearnerState)->None:
        with sqlite3.connect(self.path) as db:
            db.execute('INSERT OR REPLACE INTO learners(user_id,session_count,total_reviews) VALUES(?,?,?)',(state.user_id,state.session_count,state.total_reviews))
            db.commit()
    def get(self,user_id:str)->LearnerState|None:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT user_id,session_count,total_reviews FROM learners WHERE user_id=?',(user_id,)).fetchone()
        if row is None:return None
        state=LearnerState(row[0]); state.session_count=row[1]; state.total_reviews=row[2]; return state
