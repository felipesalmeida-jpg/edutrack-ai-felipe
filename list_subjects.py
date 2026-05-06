#!/usr/bin/env python
import requests
import json

# Configuração
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti"
AUTH_TOKEN = "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.5lwdalB63mIj9bs8QV-Z9aV2tdORsGL-bdGyutRUA4AWJM9XXXyRnI7PSmRlqH1YcRkurrt3HBzb2s8HqQ29hKBMdzPpCHhv.m_obolQXNlI41lEOc0rcPw.yPlHXzKTtlBlabtcc53lcO_8FOUeR8DdpHmAIsbU1V5mHbzEF7FfFwhr-qLSGtBZ4SuVm-5GgRq7WG_JbP_nnHV2qg4X3eyvdsfEw0aUrm9WJy7wnQUPL60fJITvg7bzTe6LqHyiFH2OEEhNY2JsPuRSgz7N-K0z1Q7xs6jACeA.TvckQiq_f4_BEH2deMoO-fm7hOE42PLIuFOtGi5vH_0"

# URL da API
url = f"{XANO_BASE_URL}/subjects"

# Headers
headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

# Fazer requisição GET
print("Listando todas as disciplinas...")

try:
    response = requests.get(url, headers=headers)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        disciplinas = response.json()
        if isinstance(disciplinas, list):
            print(f"\nTotal de disciplinas: {len(disciplinas)}\n")
            for disc in disciplinas:
                print(f"ID: {disc.get('id')} | Nome: {disc.get('name')} | Professor: {disc.get('professor')} | Dia: {disc.get('day_of_week')}")
        else:
            print(f"Resposta: {json.dumps(disciplinas, indent=2)}")
    else:
        print(f"Response Body: {response.text}")
        
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
    import traceback
    traceback.print_exc()
