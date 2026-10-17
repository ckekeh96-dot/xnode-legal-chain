from fastapi.testclient import TestClient
import hashlib,json
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_sessions_and_revocation():
 first=auth('demo1');second=auth('demo1')
 sessions=first.get('/api/security/sessions')
 assert sessions.status_code==200
 assert any(x['current'] for x in sessions.json())
 assert len(sessions.json())>=2
 assert first.post('/api/security/revoke-other-sessions').json()['revoked_count']>=1
 assert first.get('/api/security/sessions').status_code==200
 assert second.get('/api/security/sessions').status_code==401
 third=auth('demo1')
 current=[x for x in third.get('/api/security/sessions').json() if x['current']][0]
 assert third.post('/api/security/revoke-session',json={'session_id':current['session_id']}).status_code==200
 assert third.get('/api/security/sessions').status_code==401
def test_audit_report_permissions_and_digest():
 assert auth('demo1').get('/api/security/audit-report').status_code==403
 ceo=auth('demo14')
 assert ceo.get('/api/security/audit-report?limit=501').status_code==422
 r=ceo.get('/api/security/audit-report?limit=10')
 assert r.status_code==200
 obj=r.json()
 digest=hashlib.sha256(json.dumps(obj['report'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert digest==obj['sha256']
