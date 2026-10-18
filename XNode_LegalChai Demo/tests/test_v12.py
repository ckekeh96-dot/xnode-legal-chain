from fastapi.testclient import TestClient
from app import app
def auth(name):
 c=TestClient(app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_agreement_review_requires_different_reviewer():
 a=auth('demo1')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Synthetic Terms','content':'Synthetic agreement for unit testing only.'})
 assert r.status_code==200
 aid=r.json()['id']
 assert a.get('/api/agreements/'+aid+'/verify').json()['matches'] is True
 assert a.post('/api/agreements/'+aid+'/decision',json={'decision':'approve'}).status_code==409
 assert a.post('/api/agreements/'+aid+'/decision',json={'decision':'submit'}).status_code==200
 assert a.post('/api/agreements/'+aid+'/decision',json={'decision':'approve'}).status_code==403
 ceo=auth('demo14')
 assert ceo.post('/api/agreements/'+aid+'/decision',json={'decision':'approve'}).status_code==200
 assert ceo.get('/api/agreements/'+aid+'/verify').json()['anchored_on_blockchain'] is False
def test_agreement_department_scope():
 a=auth('demo1');b=auth('demo2')
 r=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Private Sample','content':'Synthetic agreement for access testing.'})
 assert r.status_code==200
 aid=r.json()['id']
 assert b.get('/api/agreements/'+aid).status_code==403
 assert b.post('/api/agreements/'+aid+'/decision',json={'decision':'submit'}).status_code==403
 assert all(x['id']!=aid for x in b.get('/api/agreements').json())
