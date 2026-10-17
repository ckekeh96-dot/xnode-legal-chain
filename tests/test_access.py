import os,tempfile,unittest,sys
from pathlib import Path
from fastapi.testclient import TestClient

class AccessTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import app;cls.app=app;cls.client=TestClient(app.app)
 def login(self,n):
  c=TestClient(self.app.app);r=c.post('/api/login',json={'username':f'demo{n}','password':'DemoOnly!2026'});self.assertEqual(r.status_code,200);return c
 def test_login_invalid(self):self.assertEqual(self.client.post('/api/login',json={'username':'demo14','password':'bad'}).status_code,401)
 def test_unauthenticated(self):self.assertEqual(self.client.get('/api/matters').status_code,401)
 def test_hr_finance_separation(self):
  hr=self.login(13);fin=self.login(12)
  self.assertEqual(hr.get('/api/hr').status_code,200);self.assertEqual(hr.get('/api/finance').status_code,403);self.assertEqual(hr.get('/api/audit').status_code,403)
  self.assertEqual(fin.get('/api/finance').status_code,200);self.assertEqual(fin.get('/api/hr').status_code,403);self.assertEqual(fin.get('/api/audit').status_code,403)
 def test_department_separation(self):
  d=self.login(1);self.assertEqual(len(d.get('/api/matters').json()),1)
  self.assertEqual(d.post('/api/matters',json={'department':self.app.DEPTS[1],'title':'Forbidden','client':'Synthetic'}).status_code,403)
  self.assertEqual(d.get('/api/finance').status_code,403)
 def test_ceo(self):
  c=self.login(14);self.assertEqual(len(c.get('/api/matters').json()),9)
  self.assertEqual(c.get('/api/hr').status_code,200);self.assertEqual(c.get('/api/finance').status_code,200);self.assertEqual(c.get('/api/audit').status_code,200)
 def test_document_share(self):
  a=self.login(1);b=self.login(2)
  r=a.post('/api/documents/MAT-0001',files={'file':('test.txt',b'synthetic content','text/plain')});self.assertEqual(r.status_code,200);did=r.json()['id']
  self.assertEqual(b.get('/api/documents/'+did+'/download').status_code,403)
  self.assertEqual(a.post('/api/shares',json={'document_id':did,'target':self.app.HR}).status_code,403)
  sid=a.post('/api/shares',json={'document_id':did,'target':self.app.DEPTS[1]}).json()['id']
  self.assertEqual(b.post('/api/shares/'+sid+'/decision',json={'status':'Approved'}).status_code,403)
  self.assertEqual(a.post('/api/shares/'+sid+'/decision',json={'status':'Approved'}).status_code,200)
  self.assertEqual(b.get('/api/documents/'+did+'/download').status_code,200)
