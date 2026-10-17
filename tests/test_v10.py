from fastapi.testclient import TestClient
from app import app
def login(name):
 c=TestClient(app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_smart_contracts_auth_and_scope():
 assert TestClient(app).get('/api/smart-contracts').status_code==401
 a,b=login('demo1'),login('demo2')
 payload={'matter_id':'MAT-0001','template':'agreement_registry'}
 assert b.post('/api/smart-contracts/build',json=payload).status_code==403
 r=a.post('/api/smart-contracts/build',json=payload)
 assert r.status_code==200
 assert 'contract AgreementRegistry' in r.json()['source']
 assert r.json()['sha256']
 assert all(x['matter_id']!='MAT-0001' for x in b.get('/api/smart-contracts').json())
def test_templates_are_non_deploying():
 a=login('demo1')
 r=a.post('/api/smart-contracts/build',json={'matter_id':'MAT-0001','template':'milestone_escrow'})
 assert r.status_code==200
 assert 'contract MilestoneEscrow' in r.json()['source']
 assert 'No deployment' in r.json()['notice']
 assert a.post('/api/smart-contracts/build',json={'matter_id':'MAT-0001','template':'unknown'}).status_code==422
