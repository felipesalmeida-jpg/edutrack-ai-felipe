import requests
import json

email = 'felipe.salmeida@aluno.impacta.edu.br'
password = 'felipe@5458'
url = 'https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti/auth/login'

data = {
    'email': email,
    'password': password
}

print('[INFO] Testando login na API...')

try:
    response = requests.post(url, json=data)
    print(f'[INFO] Status: {response.status_code}')
    resp_json = response.json()
    print(json.dumps(resp_json, indent=2))
    
    if response.status_code == 200:
        token = resp_json.get('authToken', 'N/A')
        print(f'\n[SUCESSO] Token recebido')
except Exception as e:
    print(f'[ERRO] {e}')
