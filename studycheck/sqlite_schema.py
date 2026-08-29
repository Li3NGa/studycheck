from __future__ import annotations
import sqlite3

def init_schema(db:sqlite3.Connection)->None:
    db.executescript('''
    CREATE TABLE IF NOT EXISTS learners(user_id TEXT PRIMARY KEY, session_count INTEGER NOT NULL DEFAULT 0, total_reviews INTEGER NOT NULL DEFAULT 0, payload TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS learning_events(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, knowledge_point TEXT NOT NULL, correct INTEGER NOT NULL, transfer INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_learning_events_user ON learning_events(user_id,created_at);
    ''')
