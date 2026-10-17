from fastapi.testclient import TestClient
import hashlib
import secrets
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_intent_submission_reconciliation(monkeypatch):
 ceo=auth('demo14');staff=auth('demo1')
 content='Synthetic approved registration for reconciliation.'
 aid=staff.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Reconcile test','content':content}).json()['id']
 staff.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'})
 assert ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 code='0x6001600055';addr='0x'+'b'*40
 artifact={'name':'Reconcile registry','address':addr,'runtime_codehash':'0x'+mod.keccak256(bytes.fromhex(code[2:])).hex(),'abi':[{'type':'function','name':'register','inputs':[{'type':'bytes32'},{'type':'bytes32'}]},{'type':'function','name':'verify','inputs':[{'type':'bytes32'},{'type':'bytes32'}]}]}
 artifact_id=ceo.post('/api/blockchain/registry-artifacts',json=artifact).json()['id']
 intent=ceo.post('/api/blockchain/tx-intents',json={'agreement_id':aid,'artifact_id':artifact_id}).json()['id']
 path=f'/api/blockchain/tx-intents/{intent}'
 ceo.post(path+'/approve',json={'confirmation':'I AUTHORIZE PREPARATION FOR BASE SEPOLIA TESTNET'})
 request=ceo.get(path+'/unsigned-request').json()['request']
 txhash='0x'+secrets.token_hex(32)
 assert staff.post(path+'/submitted',json={'transaction_hash':txhash}).status_code==403
 assert ceo.post(path+'/submitted',json={'transaction_hash':txhash}).status_code==200
 assert ceo.post(path+'/submitted',json={'transaction_hash':txhash}).status_code==200
 def rpc(method,params):
  return {'eth_chainId':hex(84532),'eth_getTransactionByHash':{'hash':txhash,'to':addr,'input':request['data'],'value':'0x0'},
  'eth_getTransactionReceipt':{'transactionHash':txhash,'status':'0x1','to':addr,'blockNumber':'0x64'},
  'eth_blockNumber':'0x66','eth_getCode':code}[method]
 monkeypatch.setattr(mod,'base_sepolia_rpc',rpc)
 r=ceo.get(path+'/reconcile')
 assert r.status_code==200 and r.json()['verified'] is True
 assert r.json()['broadcast_by_app'] is False
 monkeypatch.setattr(mod,'base_sepolia_rpc',lambda method,params:'0x65' if method=='eth_blockNumber' else rpc(method,params))
 assert ceo.get(path+'/reconcile').json()['status']=='awaiting_confirmations'
