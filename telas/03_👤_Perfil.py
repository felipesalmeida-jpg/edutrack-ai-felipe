import streamlit as st
import requests
import time
from PIL import Image  # <-- Biblioteca para manipulação de imagem adicionada aqui

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# ---------------------------------------------------------
# CONFIGURAÇÕES E CSS
# ---------------------------------------------------------
# Oculta instruções padrão e o ícone de olho extra do navegador (Edge/Chrome)
css_customizado = """
<style>
    [data-testid='InputInstructions'] {display: none !important;}
    
    /* Esconde o olho do Microsoft Edge/IE */
    input[type="password"]::-ms-reveal,
    input[type="password"]::-ms-clear {
        display: none !important;
    }
</style>
"""
st.markdown(css_customizado, unsafe_allow_html=True)

# URL base do grupo "Members & Accounts"
XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:ptoByL_8"
headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}

# CREDENCIAIS DE FÁBRICA PARA O RESET
EMAIL_ORIGINAL = "felipe.salmeida@aluno.impacta.edu.br"
SENHA_ORIGINAL = "felipe@5458"

# ---------------------------------------------------------
# INTERFACE DO PERFIL E UPLOAD DE FOTO
# ---------------------------------------------------------

# Inicia a memória para a foto de perfil
if "foto_perfil" not in st.session_state:
    st.session_state.foto_perfil = None

# Expansor para fazer o upload da foto que você quer colocar
with st.expander("📷 Alterar Foto de Perfil"):
    arquivo_foto = st.file_uploader("Faça upload da sua foto (PNG, JPEG)", type=['png', 'jpeg', 'jpg'])
    
    if arquivo_foto is not None:
        st.session_state.foto_perfil = Image.open(arquivo_foto)
        st.success("Foto atualizada na tela!")

# Layout Lado a Lado (Foto + Título)
col_foto, col_texto = st.columns([1, 5])

with col_foto:
    if st.session_state.foto_perfil is not None:
        st.image(st.session_state.foto_perfil, width=80)
    else:
        st.markdown("<h1 style='margin:0; padding:0; font-size: 65px; line-height: 1;'>👤</h1>", unsafe_allow_html=True)

with col_texto:
    # Mudamos de "Meu Perfil" para o seu nome. 
    # Usei <h2> para o texto mais longo não quebrar a linha e ajustei o padding para alinhar com a foto.
    st.markdown("<h2 style='margin:0; padding:0; padding-top: 22px;'>Olá, Felipe Santos de Almeida</h2>", unsafe_allow_html=True)

st.markdown("---")

# Dados Acadêmicos (A saudação foi removida daqui, ficando apenas os dados técnicos)
st.info("**RA:** 2202862")
st.write("**Curso:** Superior de Tecnologia em Análise e Desenvolvimento de Sistemas")

st.markdown("---")
st.subheader("🔐 Alterar Credenciais de Acesso")

with st.form("form_perfil", clear_on_submit=True):
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
                payload = {
                    "email": novo_email, 
                    "password": nova_senha
                }
                
                update_res = requests.patch(f"{XANO_BASE_URL}/user/edit_profile", json=payload, headers=headers)
                
                if update_res.status_code == 200:
                    st.success("✅ Credenciais atualizadas com sucesso!")
                    time.sleep(2)
                    st.session_state.auth_token = ""
                    st.rerun()
                else:
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
            
            print(f"\n[DEBUG RESET] Enviando para Xano: {payload_reset}")
            
            reset_res = requests.patch(f"{XANO_BASE_URL}/user/edit_profile", json=payload_reset, headers=headers)
            
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