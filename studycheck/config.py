from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    host: str='127.0.0.1'
    port: int=8001
    max_queue: int=20

def load_settings()->Settings:
    return Settings(
        host=os.getenv('STUDYCHECK_HOST','127.0.0.1'),
        port=int(os.getenv('STUDYCHECK_PORT','8001')),
        max_queue=int(os.getenv('STUDYCHECK_MAX_QUEUE','20')),
    )
