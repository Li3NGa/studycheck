from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import StudyCheckService
from .http_api import APIError,daily_queue,progress,review
from .sqlite_store import SQLiteLearnerRepository
from .config import load_settings

settings=load_settings()
service=StudyCheckService(SQLiteLearnerRepository(settings.db_path))

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try:
            size=int(self.headers.get('Content-Length','0') or 0)
            if size>settings.max_body_bytes: raise APIError(413,'body_too_large','request body too large')
            return json.loads(self.rfile.read(size))
        except APIError: raise
        except (ValueError,json.JSONDecodeError) as exc: raise APIError(400,'invalid_json','request body must be valid JSON') from exc
    def do_GET(self):
        try:
            if self.path=='/health':return self._send(200,{"status":"ok","service":"studycheck"})
            parts=self.path.split('/')
            if len(parts)==5 and parts[:4]==['','api','v1','users'] and parts[4]:return self._send(200,daily_queue(service,parts[4]))
            if len(parts)==6 and parts[:5]==['','api','v1','users',parts[4]] and parts[5]=='progress':return self._send(200,progress(service,parts[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
    def do_POST(self):
        try:
            if self.path=='/api/v1/reviews':return self._send(200,review(service,self._body()))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})

def run(host=None,port=None):
    host=host or settings.host; port=int(port or settings.port); HTTPServer((host,port),Handler).serve_forever()
