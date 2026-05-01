import streamlit as st
import requests
import os

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Título Principal
st.title("🎓 EduTrack AI")

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")

# Inicializa o estado de autenticação SEMPRE vazio para obrigar o login manual
if "auth_token" not in st.session_state:
    st.session_state.auth_token = ""

# ---------------------------------------------------------
# FLUXO 1: TELA DE LOGIN (Bloqueia o acesso sem autenticação)
# ---------------------------------------------------------
if not st.session_state.auth_token:
    
    # TRUQUE DE CSS: Esconde a barra lateral apenas na tela de login
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {display: none;}
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🔑 Acesso Restrito")
    st.write("Faça login com sua conta acadêmica para acessar o painel.")
    
    with st.form("login_form"):
        # Campos de texto vazios exigindo digitação manual
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        
        submit_btn = st.form_submit_button("Entrar no Sistema")
        
        if submit_btn:
            try:
                # Validação no Backend Xano
                auth_url = f"{XANO_BASE_URL}/auth/login"
                response = requests.post(auth_url, json={"email": email, "password": password})
                
                if response.status_code == 200:
                    st.session_state.auth_token = response.json().get("authToken")
                    st.success("Login realizado com sucesso! Carregando...")
                    st.rerun() # Recarrega a página para liberar o Dashboard
                else:
                    st.error("Acesso Negado. E-mail ou senha incorretos.")
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")

# ---------------------------------------------------------
# FLUXO 2: APLICAÇÃO AUTENTICADA (Só aparece após o login)
# ---------------------------------------------------------
else:
    # Sidebar - Botão de Logout
    # Como não tem o CSS escondendo aqui, a barra lateral aparece normalmente!
    st.sidebar.header("Painel de Controle")
    
    if st.sidebar.button("Sair (Logout)"):
        st.session_state.auth_token = ""
        st.rerun() # Limpa o token e volta imediatamente para a tela de login vazia

    # Dashboard Principal
    st.write("👋 Bem-vindo ao seu assistente acadêmico!")
    st.info("Utilize o menu lateral para navegar entre suas Disciplinas e Tarefas.")
    
    # Métricas Visuais de Resumo
    col1, col2 = st.columns(2)
    col1.metric("Disciplinas Ativas", "0")
    col2.metric("Tarefas Pendentes", "0")