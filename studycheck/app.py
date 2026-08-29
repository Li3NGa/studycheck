from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import StudyCheckService
from .http_api import APIError,daily_queue,review
from .store import MemoryLearnerRepository

service=StudyCheckService(MemoryLearnerRepository())

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/health': return self._send(200,{"status":"ok","service":"studycheck"})
        parts=self.path.split('/')
        if len(parts)==5 and parts[:4]==['','api','v1','users'] and parts[4]:
            try: return self._send(200,daily_queue(service,parts[4]))
            except APIError as e: return self._send(e.status,{"error":e.code,"message":e.message})
        return self._send(404,{"error":"not_found"})

def run(host='127.0.0.1',port=8001): HTTPServer((host,port),Handler).serve_forever()
