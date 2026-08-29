from __future__ import annotations
import os
from .api import StudyCheckService
from .sqlite_store import SQLiteLearnerRepository

def build_service()->StudyCheckService:
    return StudyCheckService(SQLiteLearnerRepository(os.getenv('STUDYCHECK_DB','studycheck.db')))
