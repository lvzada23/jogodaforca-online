import requests
from urllib.parse import urljoin

BASE = 'http://127.0.0.1:5000'

s = requests.Session()

print('Acessando raiz...')
r = s.get(BASE + '/')
print('Root status:', r.status_code)

# 1) Registrar usuário
email = 'test_user@example.com'
password = 'TestPass123'
name = 'Test User'

print('Registrando usuário...')
r = s.post(urljoin(BASE, '/auth/register'), data={'name': name, 'email': email, 'password': password}, allow_redirects=True)
print('Register status:', r.status_code)

# 2) Login
print('Fazendo login...')
r = s.post(urljoin(BASE, '/auth/login'), data={'email': email, 'password': password}, allow_redirects=True)
print('Login status:', r.status_code)
print('After login, redirected to:', r.url)

# 3) Criar uma partida singleplayer (POST /menu/)
print('Criando partida singleplayer...')
r = s.post(urljoin(BASE, '/menu/'), data={'mode': 'singleplayer', 'difficulty': 'easy'}, allow_redirects=True)
print('Create game status:', r.status_code)
print('Final URL after create:', r.url)

# 4) Mostrar parte do HTML retornado
print('Primeiros 500 chars da resposta final:')
print(r.text[:500])

# 5) Lista de cookies
print('Cookies:', s.cookies.get_dict())
