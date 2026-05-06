#!/usr/bin/env python
import requests
import json

# Configuração
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti"
AUTH_TOKEN = "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.5lwdalB63mIj9bs8QV-Z9aV2tdORsGL-bdGyutRUA4AWJM9XXXyRnI7PSmRlqH1YcRkurrt3HBzb2s8HqQ29hKBMdzPpCHhv.m_obolQXNlI41lEOc0rcPw.yPlHXzKTtlBlabtcc53lcO_8FOUeR8DdpHmAIsbU1V5mHbzEF7FfFwhr-qLSGtBZ4SuVm-5GgRq7WG_JbP_nnHV2qg4X3eyvdsfEw0aUrm9WJy7wnQUPL60fJITvg7bzTe6LqHyiFH2OEEhNY2JsPuRSgz7N-K0z1Q7xs6jACeA.TvckQiq_f4_BEH2deMoO-fm7hOE42PLIuFOtGi5vH_0"
SUBJECT_ID = 1  # ID da disciplina "Python Avançado"

# URL da API
url = f"{XANO_BASE_URL}/subjects/{SUBJECT_ID}"

# Headers
headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

# Fazer requisição DELETE
print(f"Deletando disciplina com id {SUBJECT_ID} (Python Avançado)...")
print(f"URL: {url}")

try:
    response = requests.delete(url, headers=headers)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Body: {response.text if response.text else '(empty)'}")
    
    if response.status_code == 200:
        print(f"\n✅ Disciplina com id {SUBJECT_ID} (Python Avançado) foi deletada com sucesso!")
    else:
        print(f"\n⚠️ Status: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Erro na conexão: {e}")
    import traceback
    traceback.print_exc()
