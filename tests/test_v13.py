from fastapi.testclient import TestClient
from app import app
def auth(name):
 c=TestClient(app)
 assert c.post('/api/login',json={'username':name,'password':'DemoOnly!2026'}).status_code==200
 return c
def test_evidence_and_pdf_after_approval():
 a=auth('demo1')
 b=auth('demo14')
 x=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Sample Agreement','content':'Synthetic agreement text for test.\nNo real parties.'})
 assert x.status_code==200
 aid=x.json()['id']
 assert a.post(f'/api/agreements/{aid}/acknowledge',json={'statement':'I have reviewed this approved agreement version'}).status_code==409
 assert a.post(f'/api/agreements/{aid}/decision',json={'decision':'submit'}).status_code==200
 assert b.post(f'/api/agreements/{aid}/decision',json={'decision':'approve'}).status_code==200
 ack=a.post(f'/api/agreements/{aid}/acknowledge',json={'statement':'I have reviewed this approved agreement version'})
 assert ack.status_code==200
 assert a.post(f'/api/agreements/{aid}/acknowledge',json={'statement':'I have reviewed this approved agreement version'}).status_code==409
 ev=a.get(f'/api/agreements/{aid}/evidence').json()
 assert ev['content_integrity_matches'] and not ev['blockchain_anchored']
 assert len(ev['acknowledgements'])==1
 pdf=a.get(f'/api/agreements/{aid}/pdf')
 assert pdf.status_code==200
 assert pdf.content.startswith(b'%PDF')
 assert len(pdf.content)>500
def test_evidence_is_department_restricted():
 a=auth('demo1');other=auth('demo2')
 x=a.post('/api/agreements',json={'matter_id':'MAT-0001','title':'Restricted','content':'Synthetic agreement for restriction test.'})
 aid=x.json()['id']
 assert other.get(f'/api/agreements/{aid}/pdf').status_code==403
 assert other.get(f'/api/agreements/{aid}/evidence').status_code==403
 assert other.post(f'/api/agreements/{aid}/acknowledge',json={'statement':'I have reviewed this approved agreement version'}).status_code==403
