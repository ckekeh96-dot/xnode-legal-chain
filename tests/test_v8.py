from fastapi.testclient import TestClient
from app import app
def test_cross_origin_blocked():
 c=TestClient(app)
 r=c.post('/api/login',headers={'Origin':'https://evil.example'},json={'username':'demo1','password':'DemoOnly!2026'})
 assert r.status_code==403
def test_login_and_cookie_flags():
 c=TestClient(app)
 r=c.post('/api/login',json={'username':'demo1','password':'DemoOnly!2026'})
 assert r.status_code==200
 assert 'httponly' in r.headers['set-cookie'].lower()
 assert 'samesite=strict' in r.headers['set-cookie'].lower()
def test_login_throttling():
 from app import LOGIN_ATTEMPTS
 LOGIN_ATTEMPTS.clear()
 c=TestClient(app)
 for _ in range(8):
  assert c.post('/api/login',json={'username':'nonexistent-user','password':'wrong'}).status_code==401
 assert c.post('/api/login',json={'username':'nonexistent-user','password':'wrong'}).status_code==429
 LOGIN_ATTEMPTS.clear()
