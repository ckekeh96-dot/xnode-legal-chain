from fastapi.testclient import TestClient
import app as mod

def auth(name):
 c=TestClient(mod.app)
 r=c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'})
 assert r.status_code==200
 return c,r.json()['csrf_token']

def test_csrf_opt_in(monkeypatch):
 c,csrf=auth('demo1')
 monkeypatch.setenv('XNODE_ENFORCE_CSRF','1')
 assert c.post('/api/security/revoke-other-sessions').status_code==403
 assert c.post('/api/security/revoke-other-sessions',headers={'X-XNode-CSRF':csrf}).status_code==200
 monkeypatch.delenv('XNODE_ENFORCE_CSRF')

def test_audit_chain_verification_and_detection():
 ceo,_=auth('demo14')
 assert ceo.get('/api/security/audit-chain-verify').status_code==200
 assert ceo.get('/api/security/audit-chain-verify').json()['valid'] is True
 other,_=auth('demo1')
 assert other.get('/api/security/audit-chain-verify').status_code==403
 with mod.db() as c:
  row=c.execute('SELECT seq FROM audit_chain ORDER BY seq DESC LIMIT 1').fetchone()
  assert row is not None
  c.execute('UPDATE audit_chain SET action=? WHERE seq=?',('tampered',row['seq']))
 assert ceo.get('/api/security/audit-chain-verify').json()['valid'] is False
 with mod.db() as c:
  # restore only for isolated test DB cleanup; recompute hash from canonical original
  row=c.execute('SELECT event_id,actor,resource,ts,prev_hash FROM audit_chain WHERE seq=?',(row['seq'],)).fetchone()
  original=c.execute('SELECT action FROM audit WHERE id=?',(row['event_id'],)).fetchone()['action']
  import json,hashlib
  digest=hashlib.sha256(json.dumps([row['event_id'],row['actor'],original,row['resource'],row['ts'],row['prev_hash']],separators=(',',':')).encode()).hexdigest()
  c.execute('UPDATE audit_chain SET action=?,entry_hash=? WHERE seq=?',(original,digest,c.execute('SELECT MAX(seq) FROM audit_chain').fetchone()[0]))
