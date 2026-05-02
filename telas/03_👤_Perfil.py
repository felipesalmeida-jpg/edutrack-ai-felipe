import streamlit as st
import requests
import time

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# ---------------------------------------------------------
# CONFIGURAÇÕES E CSS
# ---------------------------------------------------------
st.markdown("<style>[data-testid='InputInstructions'] {display: none !important;}</style>", unsafe_allow_html=True)

# URL base do grupo "Members & Accounts" que você encontrou
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:ptoByL_8"
headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}

# CREDENCIAIS DE FÁBRICA PARA O RESET
EMAIL_ORIGINAL = "felipe.salmeida@aluno.impacta.edu.br"
SENHA_ORIGINAL = "felipe@5458"

# ---------------------------------------------------------
# INTERFACE DO PERFIL
# ---------------------------------------------------------
st.title("👤 Meu Perfil")

# Dados Acadêmicos do Felipe Santos de Almeida
st.markdown("### Olá, Felipe Santos de Almeida")
st.info("**RA:** 2202862")
st.write("**Curso:** Superior de Tecnologia em Análise e Desenvolvimento de Sistemas")

st.markdown("---")
st.subheader("🔐 Alterar Credenciais de Acesso")

with st.form("form_perfil", clear_on_submit=True):
    # Dica: O Xano também aceita 'name' nesse endpoint se você quiser adicionar depois
    novo_email = st.text_input("Novo E-mail", placeholder="Ex: felipe.santos122@gmail.com")
    nova_senha = st.text_input("Nova Senha", type="password", placeholder="Digite a nova senha")
    confirmacao = st.text_input("Confirme a Senha", type="password")
    
    submit = st.form_submit_button("Salvar e Sincronizar")

    if submit:
        if not novo_email or not nova_senha:
            st.warning("Preencha todos os campos.")
        elif nova_senha != confirmacao:
            st.error("As senhas não coincidem.")
        else:
            try:
                # O payload deve bater com os inputs que você viu no vídeo (email e password)
                payload = {
                    "email": novo_email, 
                    "password": nova_senha
                }
                
                # Chamada para o endpoint edit_profile que você copiou
                update_res = requests.patch(f"{XANO_BASE_URL}/user/edit_profile", json=payload, headers=headers)
                
                if update_res.status_code == 200:
                    st.success("✅ Credenciais atualizadas com sucesso!")
                    time.sleep(2)
                    st.session_state.auth_token = ""
                    st.rerun()
                else:
                    # Exibe o erro real do Xano para facilitar o seu debug
                    st.error(f"Erro no Xano: {update_res.text}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

# ---------------------------------------------------------
# BARRA LATERAL: RESTAURAÇÃO
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Restauração")

if st.sidebar.button("Reset de Credenciais"):
    st.sidebar.warning("Isso voltará para os dados originais da Impacta. Confirmar?")
    
if st.sidebar.button("✅ Confirmar Reset"):
        try:
            payload_reset = {"email": EMAIL_ORIGINAL, "password": SENHA_ORIGINAL}
            
            # DEBUG: Mostra o que está sendo enviado para o terminal
            print(f"\n[DEBUG RESET] Enviando para Xano: {payload_reset}")
            
            reset_res = requests.patch(f"{XANO_BASE_URL}/user/edit_profile", json=payload_reset, headers=headers)
            
            # DEBUG: Mostra a resposta real do Xano no VS Code
            print(f"[DEBUG RESET] Status: {reset_res.status_code}")
            print(f"[DEBUG RESET] Resposta: {reset_res.text}")
            
            if reset_res.status_code == 200:
                st.sidebar.success("✅ Reset concluído!")
                time.sleep(2)
                st.session_state.auth_token = ""
                st.rerun()
            else:
                st.sidebar.error(f"Erro no Xano: {reset_res.status_code}")
        except Exception as e:
            st.sidebar.error(f"Erro no reset: {e}")
            