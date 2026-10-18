from fastapi.testclient import TestClient
from app import app,connect
import hashlib
def test_session_persisted_hashed():
 c=TestClient(app)
 r=c.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'})
 assert r.status_code==200
 token=c.cookies.get('xnode_session')
 with connect() as db:
  assert db.execute('SELECT 1 FROM sessions WHERE token_hash=?',(hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
  assert not db.execute('SELECT 1 FROM sessions WHERE token_hash=?',(token,)).fetchone()
 assert c.get('/api/me').status_code==200
 assert c.post('/api/logout').status_code==200
 assert c.get('/api/me').status_code==401
def test_security_activity_department_scope():
 a=TestClient(app);b=TestClient(app)
 assert a.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'}).status_code==200
 assert b.post('/api/login',json={'username':'demo2','password':'DemoOnly!2026'}).status_code==200
 assert all(x['username']=='demo1' for x in a.get('/api/security/activity').json())
