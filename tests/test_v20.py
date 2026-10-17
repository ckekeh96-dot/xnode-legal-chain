from fastapi.testclient import TestClient
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_external_deployment_tracking(monkeypatch):
 ceo=auth('demo14');staff=auth('demo1')
 code='0x6001600055';address='0x'+'a'*40;txhash='0x'+'b'*64
 artifact={'name':'Deployment tracking test','address':address,'runtime_codehash':'0x'+mod.keccak256(bytes.fromhex(code[2:])).hex(),'abi':[{'type':'function','name':'verify'},{'type':'function','name':'register'}]}
 a=ceo.post('/api/blockchain/registry-artifacts',json=artifact).json()['id']
 url=f'/api/blockchain/registry-artifacts/{a}/track-deployment'
 assert staff.post(url,json={'transaction_hash':txhash}).status_code==403
 r=ceo.post(url,json={'transaction_hash':txhash})
 assert r.status_code==200 and r.json()['broadcast_by_app'] is False
 tid=r.json()['id']
 assert ceo.post(url,json={'transaction_hash':txhash}).json()['id']==tid
 assert staff.get(f'/api/blockchain/deployment-tracks/{tid}/status').status_code==403
 def rpc(method,params):
  return {'eth_chainId':hex(84532),'eth_getTransactionByHash':{'hash':txhash,'to':None},
  'eth_getTransactionReceipt':{'transactionHash':txhash,'status':'0x1','contractAddress':address,'blockNumber':'0x64'},
  'eth_blockNumber':'0x66','eth_getCode':code}[method]
 monkeypatch.setattr(mod,'base_sepolia_rpc',rpc)
 r=ceo.get(f'/api/blockchain/deployment-tracks/{tid}/status')
 assert r.status_code==200 and r.json()['verified'] is True
 assert r.json()['confirmations']==3
 monkeypatch.setattr(mod,'base_sepolia_rpc',lambda method,params:'0x65' if method=='eth_blockNumber' else rpc(method,params))
 assert ceo.get(f'/api/blockchain/deployment-tracks/{tid}/status').json()['status']=='awaiting_confirmations'
