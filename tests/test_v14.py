from fastapi.testclient import TestClient
from app import app
def auth(name):
 c=TestClient(app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def approved():
 a=auth('demo1');ceo=auth('demo14')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Synthetic Client Draft','content':'Synthetic agreement, not a legal document.'})
 aid=r.json()['id']
 assert a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'}).status_code==200
 assert ceo.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 return a,aid
def test_one_time_invitation():
 a,aid=approved()
 r=a.post(f'/api/agreements/{aid}/client-invite',json={'recipient_label':'Demo Client','expires_hours':1})
 assert r.status_code==200
 token=r.json()['token'];anon=TestClient(app)
 assert anon.post('/api/client-portal/preview',json={'token':token}).status_code==200
 assert anon.post('/api/client-portal/respond',json={'token':token,'decision':'reviewed'}).status_code==200
 assert anon.post('/api/client-portal/respond',json={'token':token,'decision':'reviewed'}).status_code==404
 assert a.get(f'/api/agreements/{aid}/client-reviews').json()[0]['decision']=='reviewed'
def test_revoke_and_scope():
 a,aid=approved();b=auth('demo2')
 assert b.post(f'/api/agreements/{aid}/client-invite',json={'recipient_label':'No Access'}).status_code==403
 r=a.post(f'/api/agreements/{aid}/client-invite',json={'recipient_label':'Demo Client'})
 assert a.post('/api/client-invites/'+r.json()['id']+'/revoke').status_code==200
 assert TestClient(app).post('/api/client-portal/preview',json={'token':r.json()['token']}).status_code==404
 assert b.get(f'/api/agreements/{aid}/client-reviews').status_code==403
