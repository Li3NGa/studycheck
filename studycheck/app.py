from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import StudyCheckService
from .http_api import APIError,daily_queue,review
from .store import MemoryLearnerRepository
from .config import load_settings

service=StudyCheckService(MemoryLearnerRepository())

class Handler(BaseHTTPRequestHandler):
    def _send(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def _body(self):
        try:return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')) or 0))
        except (ValueError,json.JSONDecodeError):raise APIError(400,'invalid_json','request body must be valid JSON')
    def do_GET(self):
        try:
            if self.path=='/health':return self._send(200,{"status":"ok","service":"studycheck"})
            parts=self.path.split('/')
            if len(parts)==5 and parts[:4]==['','api','v1','users'] and parts[4]:return self._send(200,daily_queue(service,parts[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
    def do_POST(self):
        try:
            if self.path=='/api/v1/reviews':return self._send(200,review(service,self._body()))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})

def run(host=None,port=None):
    settings=load_settings(); HTTPServer((host or settings.host,port or settings.port),Handler).serve_forever()
