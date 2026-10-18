import os, tempfile
from pathlib import Path
os.environ.setdefault("XNODE_TEST","1")
from fastapi.testclient import TestClient
from app import app, DEPTS
def test_new_routes_require_login():
 c=TestClient(app)
 for url in ('/api/clients','/api/events','/api/templates'):
  assert c.get(url).status_code==401
def test_department_isolation():
 a=TestClient(app);b=TestClient(app)
 assert a.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'}).status_code==200
 assert b.post('/api/login',json={'username':'demo2','password':'DemoOnly!2026'}).status_code==200
 r=a.post('/api/clients',json={'department':DEPTS[0],'name':'Synthetic Test Client'})
 assert r.status_code==200
 assert all(x['id']!=r.json()['id'] for x in b.get('/api/clients').json())
 assert b.post('/api/events',json={'department':DEPTS[0],'title':'Court','starts_at':'2026-11-02T10:00'}).status_code==403
 assert b.post('/api/drafts',json={'matter_id':'MAT-0001','document_type':'matter_checklist'}).status_code==403
