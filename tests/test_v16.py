from fastapi.testclient import TestClient
import hashlib
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_testnet_verifier_gates(monkeypatch):
 a=auth('demo1');ceo=auth('demo14')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Testnet sample','content':'Synthetic text for testnet verification only.'})
 aid=r.json()['id']
 txhash='0x'+'a'*64
 assert a.post(f'/api/agreements/{aid}/verify-testnet-tx',json={'transaction_hash':txhash}).status_code==409
 assert a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'}).status_code==200
 assert ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 assert auth('demo2').post(f'/api/agreements/{aid}/verify-testnet-tx',json={'transaction_hash':txhash}).status_code==403
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_ADDRESS','0x'+'b'*40)
 expected=hashlib.sha256(aid.encode()).hexdigest()+hashlib.sha256('Synthetic text for testnet verification only.'.encode()).hexdigest()
 def fake_rpc(method,params):
  if method=='eth_chainId':return hex(84532)
  if method=='eth_getTransactionByHash':return {'to':'0x'+'b'*40,'input':'0x12345678'+expected}
  if method=='eth_getTransactionReceipt':return {'status':'0x1','blockNumber':'0x123','to':'0x'+'b'*40,'transactionHash':txhash}
 monkeypatch.setattr(mod,'base_sepolia_rpc',fake_rpc)
 v=a.post(f'/api/agreements/{aid}/verify-testnet-tx',json={'transaction_hash':txhash})
 assert v.status_code==200 and v.json()['verified'] is True
 assert v.json()['legal_validity_verified'] is False
 monkeypatch.setattr(mod,'base_sepolia_rpc',lambda method,params: '0x1' if method=='eth_chainId' else None)
 assert a.post(f'/api/agreements/{aid}/verify-testnet-tx',json={'transaction_hash':txhash}).status_code==502
