from fastapi.testclient import TestClient
import hashlib
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_keccak_known_vector():
 assert mod.keccak256(b'').hex()=='c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
def test_strict_event_and_confirmations(monkeypatch):
 a=auth('demo1');ceo=auth('demo14')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Strict event sample','content':'Synthetic agreement for strict event test.'})
 aid=r.json()['id']
 a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'})
 ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'})
 monkeypatch.setenv('XNODE_BASE_SEPOLIA_REGISTRY_ADDRESS','0x'+'b'*40)
 txhash='0x'+'a'*64
 sender='0x'+'c'*40
 idhash=hashlib.sha256(aid.encode()).hexdigest()
 doc=hashlib.sha256(b'Synthetic agreement for strict event test.').hexdigest()
 selector=mod.keccak256(b'register(bytes32,bytes32)')[:4].hex()
 event='0x'+mod.keccak256(b'Registered(bytes32,address,bytes32)').hex()
 log={'address':'0x'+'b'*40,'topics':[event,'0x'+idhash,'0x'+('c'*40).rjust(64,'0')],'data':'0x'+doc,'transactionHash':txhash}
 receipt={'status':'0x1','blockNumber':'0x64','to':'0x'+'b'*40,'transactionHash':txhash,'logs':[log]}
 def rpc(method,params):
  return {'eth_chainId':hex(84532),'eth_blockNumber':'0x67','eth_getTransactionByHash':{'to':'0x'+'b'*40,'from':sender,'input':'0x'+selector+idhash+doc},'eth_getTransactionReceipt':receipt}[method]
 monkeypatch.setattr(mod,'base_sepolia_rpc',rpc)
 url=f'/api/agreements/{aid}/verify-registry-event'
 assert a.post(url,json={'transaction_hash':txhash,'min_confirmations':4}).json()['verified'] is True
 assert a.post(url,json={'transaction_hash':txhash,'min_confirmations':5}).json()['verified'] is False
 receipt['logs']=[]
 assert a.post(url,json={'transaction_hash':txhash}).json()['verified'] is False
 assert auth('demo2').post(url,json={'transaction_hash':txhash}).status_code==403
