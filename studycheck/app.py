from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from .api import StudyCheckService
from .http_api import APIError,daily_queue,progress,review
from .upload_api import ingest_uploaded_material
from .plan_api import current_plan
from .commerce import CommerceService,SQLiteOrderRepository
from .commerce_api import pricing,create_order,checkout,confirm,entitlement
from .payment import DisabledPaymentProvider
from .sqlite_store import SQLiteLearnerRepository
from .config import load_settings

settings=load_settings()
service=StudyCheckService(SQLiteLearnerRepository(settings.db_path))
commerce=CommerceService(SQLiteOrderRepository(settings.db_path),DisabledPaymentProvider())

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
            if self.path=='/api/v1/plan':return self._send(200,current_plan(service))
            if self.path=='/api/v1/pricing':return self._send(200,pricing())
            if self.path.startswith('/api/v1/users/') and self.path.endswith('/entitlement'):
                return self._send(200,entitlement(commerce,self.path.split('/')[4]))
            parts=self.path.split('/')
            if len(parts)==5 and parts[:4]==['','api','v1','users'] and parts[4]:return self._send(200,daily_queue(service,parts[4]))
            if len(parts)==6 and parts[:5]==['','api','v1','users',parts[4]] and parts[5]=='progress':return self._send(200,progress(service,parts[4]))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
        except (KeyError,ValueError) as e:return self._send(400,{"error":"invalid_request","message":str(e)})
    def do_POST(self):
        try:
            if self.path=='/api/v1/orders': return self._send(201,create_order(commerce,self._body()))
            if self.path.startswith('/api/v1/orders/') and self.path.endswith('/checkout'):
                body=self._body(); return self._send(200,checkout(commerce,self.path.split('/')[4],str(body.get('notify_url',''))))
            if self.path.startswith('/api/v1/orders/') and self.path.endswith('/confirm'):
                body=self._body(); return self._send(200,confirm(commerce,self.path.split('/')[4],str(body.get('payload','')).encode(),str(body.get('signature',''))))
            if self.path=='/api/v1/materials/upload':return self._send(201,ingest_uploaded_material(service,self._body()))
            if self.path=='/api/v1/reviews':return self._send(200,review(service,self._body()))
            return self._send(404,{"error":"not_found"})
        except APIError as e:return self._send(e.status,{"error":e.code,"message":e.message})
        except RuntimeError as e:return self._send(503,{"error":"service_unavailable","message":str(e)})
        except (KeyError,ValueError) as e:return self._send(400,{"error":"invalid_request","message":str(e)})

def run(host=None,port=None):
    host=host or settings.host; port=int(port or settings.port); HTTPServer((host,port),Handler).serve_forever()
