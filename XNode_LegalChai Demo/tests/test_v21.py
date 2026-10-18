from fastapi.testclient import TestClient
import hashlib
import app as mod
def auth(name):
 c=TestClient(mod.app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_unsigned_intent_approval_and_cancel():
 ceo=auth('demo14');staff=auth('demo1')
 agreement=staff.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Testnet intent','content':'Synthetic approved content for an unsigned transaction intent.'}).json()['id']
 staff.post(f'/api/agreements/{agreement}/decision',json={'decision':'submit'})
 assert ceo.post(f'/api/agreements/{agreement}/decision',json={'decision':'approve'}).status_code==200
 artifact={'name':'Intent registry','address':'0x'+'b'*40,'runtime_codehash':'0x'+'1'*64,'abi':[{'type':'function','name':'register','inputs':[{'type':'bytes32'},{'type':'bytes32'}]},{'type':'function','name':'verify','inputs':[{'type':'bytes32'},{'type':'bytes32'}]}]}
 aid=ceo.post('/api/blockchain/registry-artifacts',json=artifact).json()['id']
 assert staff.post('/api/blockchain/tx-intents',json={'agreement_id':agreement,'artifact_id':aid}).status_code==403
 created=ceo.post('/api/blockchain/tx-intents',json={'agreement_id':agreement,'artifact_id':aid})
 assert created.status_code==200
 iid=created.json()['id'];path=f'/api/blockchain/tx-intents/{iid}'
 assert ceo.get(path+'/unsigned-request').status_code==409
 assert ceo.post(path+'/approve',json={'confirmation':'wrong'}).status_code==422
 assert ceo.post(path+'/approve',json={'confirmation':'I AUTHORIZE PREPARATION FOR BASE SEPOLIA TESTNET'}).status_code==200
 assert ceo.post(path+'/approve',json={'confirmation':'I AUTHORIZE PREPARATION FOR BASE SEPOLIA TESTNET'}).status_code==409
 r=ceo.get(path+'/unsigned-request')
 assert r.status_code==200
 obj=r.json()
 assert obj['request']['chainId']==84532 and obj['request']['value']=='0x0'
 assert obj['request']['data'].startswith('0x'+mod.keccak256(b'register(bytes32,bytes32)')[:4].hex())
 assert obj['signed'] is False and obj['broadcast'] is False
 assert staff.get(path+'/unsigned-request').status_code==403
 assert ceo.post(path+'/cancel').status_code==200
 assert ceo.get(path+'/unsigned-request').status_code==409
