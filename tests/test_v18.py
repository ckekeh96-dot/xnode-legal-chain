from fastapi.testclient import TestClient
import hashlib
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_current_registry_status(monkeypatch):
 a=auth('demo1');ceo=auth('demo14')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Current registry status','content':'Synthetic agreement for state testing.'})
 assert r.status_code==200
 aid=r.json()['id']
 url=f'/api/agreements/{aid}/registry-current-state'
 assert a.get(url).status_code==409
 a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'})
 ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'})
 assert auth('demo2').get(url).status_code==403
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_ADDRESS','0x'+'b'*40)
 code='0x6001600055'
 expected='0x'+mod.keccak256(bytes.fromhex(code[2:])).hex()
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_CODEHASH',expected)
 observed={}
 def rpc(method,params):
  observed[method]=params
  return {'eth_chainId':hex(84532),'eth_getCode':code,'eth_call':'0x'+('0'*63)+'1','eth_blockNumber':'0x123'}[method]
 monkeypatch.setattr(mod,'base_sepolia_rpc',rpc)
 result=a.get(url)
 assert result.status_code==200
 assert result.json()['registered'] is True
 assert result.json()['bytecode_matched'] is True
 assert observed['eth_call'][0]['data'].startswith('0x'+mod.keccak256(b'verify(bytes32,bytes32)')[:4].hex())
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_CODEHASH','0x'+'0'*64)
 assert a.get(url).json()['bytecode_matched'] is False
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_CODEHASH',expected)
 monkeypatch.setattr(mod,'base_sepolia_rpc',lambda method,params:('0x'+('0'*64)) if method=='eth_call' else rpc(method,params))
 assert a.get(url).json()['registered'] is False
