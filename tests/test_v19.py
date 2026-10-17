from fastapi.testclient import TestClient
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_artifact_access_and_read_only_verification(monkeypatch):
 ceo=auth('demo14');other=auth('demo1')
 artifact={'name':'Demo Registry','address':'0x'+'a'*40,'runtime_codehash':'0x'+mod.keccak256(bytes.fromhex('6001600055')).hex(),'abi':[{'type':'function','name':'verify'},{'type':'function','name':'register'}]}
 assert other.post('/api/blockchain/registry-artifacts',json=artifact).status_code==403
 result=ceo.post('/api/blockchain/registry-artifacts',json=artifact)
 assert result.status_code==200
 aid=result.json()['id']
 assert result.json()['verified_onchain'] is False
 assert other.get(f'/api/blockchain/registry-artifacts/{aid}/verify').status_code==403
 monkeypatch.setattr(mod,'base_sepolia_rpc',lambda method,params:{'eth_chainId':hex(84532),'eth_getCode':'0x6001600055'}[method])
 assert ceo.get(f'/api/blockchain/registry-artifacts/{aid}/verify').json()['verified'] is True
 checklist=ceo.get(f'/api/blockchain/registry-artifacts/{aid}/deployment-checklist').json()
 assert checklist['transactions_sent']==0 and checklist['wallet_connected'] is False
