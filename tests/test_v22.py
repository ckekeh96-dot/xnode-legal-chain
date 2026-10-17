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
def test_account_password_rotation():
 a=auth('demo5');other=auth('demo5')
 try:
  assert a.post('/api/account/password',json={'old_password':'DemoOnly!2026','new_password':'Rotated!2026Demo'}).status_code==200
  assert other.get('/api/me').status_code==401
  assert a.get('/api/me').status_code==200
  assert TestClient(mod.app).post('/api/login',json={'username':'demo5','password':'DemoOnly!2026'}).status_code==401
  assert a.post('/api/account/password',json={'old_password':'wrong-password','new_password':'Another!Pass2026'}).status_code==401
 finally:
  a.post('/api/account/password',json={'old_password':'Rotated!2026Demo','new_password':'DemoOnly!2026'})
 assert TestClient(mod.app).post('/api/login',json={'username':'demo5','password':'DemoOnly!2026'}).status_code==200
def test_clause_review_checks():
 staff=auth('demo1')
 text=('This agreement is governed by the laws of the republic of South Africa. '
  'Either party may terminate this agreement on 30 days written notice. '
  'Fees are payable within 30 days of invoice. '
  'Liability is unlimited and the provider may amend the terms at its sole discretion. '
  'This agreement will automatically renew each year. '
  'Payment terms: [] Amount: ____ ')
 r=staff.post('/api/review/clauses',json={'matter_id':'MAT-0001','document_text':text})
 assert r.status_code==200
 b=r.json()
 assert b['summary']['checks_run']==len(b['flags'])
 assert b['summary']['checks_run']==17
 by={f['check']:(f['status'],f['severity']) for f in b['flags']}
 assert by['Governing law & jurisdiction'][0]=='OK'
 assert by['Termination rights'][0]=='OK'
 assert by['Confidentiality']==('Missing','Medium')
 assert by['Unlimited liability']==('Review','High')
 assert by['Unilateral amendment']==('Review','High')
 assert by['Automatic renewal']==('Review','Medium')
 assert by['Unfilled placeholders']==('Review','High')
 assert b['summary']['risk']=='High'
 assert b['summary']['flagged']==sum(1 for f in b['flags'] if f['status']!='OK')
 assert staff.post('/api/review/clauses',json={'matter_id':'MAT-9999','document_text':'x'}).status_code==404
 clean=staff.post('/api/review/clauses',json={'matter_id':'MAT-0001','document_text':'Governing law: South African law. Termination, confidentiality, dispute resolution by arbitration, payment terms, POPIA data protection, force majeure, signature block, entire agreement. No risky terms here.'}).json()
 assert clean['summary']['risk'] in ('Clean','Low','Medium')
 assert all(f['status']!='Review' for f in clean['flags'])
def test_ai_assist_and_usage(monkeypatch):
 import json,urllib.request
 ceo=auth('demo14');staff=auth('demo1')
 st=ceo.get('/api/ai/status').json()
 assert st['enabled'] is False and 'Ollama' in st['provider']
 assert staff.post('/api/ai/assist',json={'matter_id':'MAT-0001','instruction':'Summarize the sample text'}).status_code==503
 def fake(req,timeout=0):
  class R:
   def __enter__(self):return self
   def __exit__(self,*a):return False
   def read(self,n):return json.dumps({'response':'DRAFT — synthetic local output for attorney review.'}).encode()
  return R()
 monkeypatch.setenv('XNODE_ENABLE_LOCAL_AI','1')
 monkeypatch.setattr(urllib.request,'urlopen',fake)
 r1=ceo.post('/api/ai/assist',json={'matter_id':'MAT-0001','instruction':'Summarize the supplied sample contract','document_text':'Synthetic sample text.'})
 r2=staff.post('/api/ai/assist',json={'matter_id':'MAT-0001','instruction':'Draft a short acknowledgement letter','document_text':''})
 assert r1.status_code==200 and r2.status_code==200
 assert 'attorney' in r1.json()['notice'].lower() and r1.json()['model']
 u=ceo.get('/api/ai/usage').json()
 assert u['total']>=2 and u['last_used'] and u['entries'][0]['resource']=='MAT-0001'
 assert u['total']==sum(u['by_user'].values())==sum(u['by_matter'].values())
 s=staff.get('/api/ai/usage').json()
 assert s['entries'] and all(e['actor']=='demo1' for e in s['entries'])
def test_v25_dashboards():
 ceo=auth('demo14');staff=auth('demo1')
 notes=staff.get('/api/notes/recent').json()
 assert isinstance(notes,list) and all('matter_title' in n for n in notes)
 nid=staff.post('/api/matters/MAT-0001/notes',json={'matter_id':'MAT-0001','body':'Synthetic dashboard test note'}).json()['id']
 assert any(n['id']==nid for n in staff.get('/api/notes/recent').json())
 assert any(n['id']==nid for n in ceo.get('/api/notes/recent').json())
 d=staff.post('/api/drafts',json={'matter_id':'MAT-0001','document_type':'matter_checklist'})
 assert d.status_code==200 and 'CHECKLIST' in d.json()['body']
 u=staff.get('/api/drafts/usage').json()
 assert u['total']>=1 and u['entries'][0]['resource']=='MAT-0001'
 assert u['total']==sum(u['by_user'].values())==sum(u['by_matter'].values())
 e=staff.post('/api/events',json={'department':'Litigation & Dispute Resolution','title':'Dashboard hearing','starts_at':'2026-12-01T09:00','location':'Court 5'}).json()
 assert any(x['id']==e['id'] for x in staff.get('/api/events').json())
 lst=ceo.get('/api/client-invites').json()
 assert set(lst)>={'invites','reviews','total','active'}
 assert all(i['status'] in ('Active','Consumed','Expired','Revoked') for i in lst['invites'])
 aid=staff.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Portal flow test','content':'Synthetic agreement text for the portal flow test.'}).json()['id']
 staff.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'})
 assert ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 inv=staff.post(f'/api/agreements/{aid}/client-invite',json={'recipient_label':'Synthetic Client 1'}).json()
 token=inv['token']
 lst=ceo.get('/api/client-invites').json()
 mine=[i for i in lst['invites'] if i['id']==inv['id']][0]
 assert mine['status']=='Active' and mine['agreement_title']=='Portal flow test' and mine['decision'] is None
 assert ceo.post('/api/client-portal/preview',json={'token':token}).status_code==200
 assert ceo.post('/api/client-portal/respond',json={'token':token,'decision':'reviewed'}).status_code==200
 mine2=[i for i in ceo.get('/api/client-invites').json()['invites'] if i['id']==inv['id']][0]
 assert mine2['status']=='Consumed' and mine2['decision']=='reviewed'
 assert ceo.post('/api/client-portal/respond',json={'token':token,'decision':'reviewed'}).status_code==404 # consumed tokens resolve as invalid; 409 is only the concurrent-race guard


