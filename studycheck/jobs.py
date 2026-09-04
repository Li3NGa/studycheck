from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Callable
import json,sqlite3
from uuid import uuid4

@dataclass(frozen=True)
class LearningJob:
    job_id:str; user_id:str; status:str; result:dict|None=None; error:str|None=None; created_at:str=''

class SQLiteJobStore:
    def __init__(self,path:str='studycheck.db'):
        self.path=path
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS learning_jobs(job_id TEXT PRIMARY KEY,user_id TEXT NOT NULL,status TEXT NOT NULL,result TEXT,error TEXT,created_at TEXT NOT NULL)'); db.commit()
    def create(self,user_id:str)->LearningJob:
        job=LearningJob(uuid4().hex,user_id,'queued',created_at=datetime.now(timezone.utc).isoformat())
        with sqlite3.connect(self.path) as db: db.execute('INSERT INTO learning_jobs VALUES(?,?,?,?,?,?)',(job.job_id,job.user_id,job.status,None,None,job.created_at)); db.commit()
        return job
    def update(self,job_id:str,status:str,result:dict|None=None,error:str|None=None)->LearningJob:
        if status not in {'queued','running','completed','failed'}: raise ValueError('invalid job status')
        with sqlite3.connect(self.path) as db:
            db.execute('UPDATE learning_jobs SET status=?,result=?,error=? WHERE job_id=?',(status,json.dumps(result,ensure_ascii=False) if result is not None else None,error,job_id)); db.commit()
        return self.get(job_id)
    def get(self,job_id:str)->LearningJob:
        with sqlite3.connect(self.path) as db: row=db.execute('SELECT job_id,user_id,status,result,error,created_at FROM learning_jobs WHERE job_id=?',(job_id,)).fetchone()
        if not row: raise KeyError(job_id)
        return LearningJob(row[0],row[1],row[2],json.loads(row[3]) if row[3] else None,row[4],row[5])

class LearningJobRunner:
    def __init__(self,store:SQLiteJobStore,runner:Callable[[str],dict]): self.store=store; self.runner=runner
    def run(self,job_id:str)->LearningJob:
        job=self.store.get(job_id); self.store.update(job_id,'running')
        try: result=self.runner(job.user_id); return self.store.update(job_id,'completed',result)
        except Exception as exc: return self.store.update(job_id,'failed',error=str(exc))
