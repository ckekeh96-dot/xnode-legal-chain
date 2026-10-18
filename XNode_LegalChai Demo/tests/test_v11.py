from fastapi.testclient import TestClient
from app import app
def test_manifest_and_compiler_gates(monkeypatch):
 c=TestClient(app)
 assert c.post('/api/smart-contracts/compile',json={'matter_id':'MAT-0001','template':'agreement_registry'}).status_code==401
 assert c.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'}).status_code==200
 r=c.post('/api/smart-contracts/build',json={'matter_id':'MAT-0001','template':'agreement_registry','agreement_title':'Sample','jurisdiction':'South Africa','document_text':'synthetic'})
 assert r.status_code==200
 assert r.json()['agreement_manifest']['title']=='Sample'
 assert len(r.json()['agreement_manifest']['document_sha256'])==64
 monkeypatch.setattr('shutil.which',lambda _:None)
 assert c.post('/api/smart-contracts/compile',json={'matter_id':'MAT-0001','template':'agreement_registry'}).status_code==503
def test_compiler_cross_department_rejected():
 c=TestClient(app)
 assert c.post('/api/login',json={'username':'demo2','password':'DemoOnly!2026'}).status_code==200
 assert c.post('/api/smart-contracts/compile',json={'matter_id':'MAT-0001','template':'agreement_registry'}).status_code==403
