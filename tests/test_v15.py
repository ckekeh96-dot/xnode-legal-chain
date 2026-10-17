from fastapi.testclient import TestClient
from app import app
import hashlib,json
def auth(name):
 c=TestClient(app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_bundle_and_unsigned_payload():
 a=auth('demo1');ceo=auth('demo14')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Evidence test','content':'This is synthetic agreement evidence only.'})
 assert r.status_code==200
 aid=r.json()['id']
 assert a.get(f'/api/agreements/{aid}/testnet-anchor-payload').status_code==409
 assert a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'}).status_code==200
 assert ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 r=a.get(f'/api/agreements/{aid}/evidence-bundle')
 assert r.status_code==200
 obj=r.json()
 canonical=json.dumps(obj['bundle'],sort_keys=True,separators=(',',':'),ensure_ascii=False)
 assert hashlib.sha256(canonical.encode()).hexdigest()==obj['bundle_sha256']
 assert obj['bundle']['blockchain_anchored'] is False
 payload=a.get(f'/api/agreements/{aid}/testnet-anchor-payload').json()
 assert payload['document_hash_bytes32']=='0x'+obj['bundle']['agreement']['content_sha256']
 assert payload['deployment_performed'] is False
 assert auth('demo2').get(f'/api/agreements/{aid}/evidence-bundle').status_code==403
