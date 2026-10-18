from fastapi.testclient import TestClient
from app import app,DEPTS
def test_ai_auth_required():
 c=TestClient(app)
 assert c.get('/api/ai/status').status_code==401
 assert c.post('/api/ai/assist',json={'matter_id':'MAT-0001','instruction':'Summarize document'}).status_code==401
def test_ai_disabled_and_scope(monkeypatch):
 monkeypatch.delenv('XNODE_ENABLE_LOCAL_AI',raising=False)
 a=TestClient(app);b=TestClient(app)
 assert a.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'}).status_code==200
 assert b.post('/api/login',json={'username':'demo2','password':'DemoOnly!2026'}).status_code==200
 x={'matter_id':'MAT-0001','instruction':'Summarize this sample document'}
 assert b.post('/api/ai/assist',json=x).status_code==403
 assert a.post('/api/ai/assist',json=x).status_code==503
 assert a.get('/api/ai/status').json()['enabled'] is False
def test_security_headers():
 r=TestClient(app).get('/')
 assert r.headers['x-content-type-options']=='nosniff'
 assert r.headers['x-frame-options']=='DENY'
