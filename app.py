import streamlit as st
import requests
import os

# 1. Configuração da Página
st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Inicializa o estado de autenticação vazio
if "auth_token" not in st.session_state:
    st.session_state.auth_token = ""

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")

# ---------------------------------------------------------
# FUNÇÃO DA TELA DE LOGIN (Só existe se não houver acesso)
# ---------------------------------------------------------
def tela_login():
    # TRUQUE DE CSS: Esconde o texto de Enter e o "olho" duplicado do navegador
    st.markdown(
        """
        <style>
            /* Esconde o "Press Enter to submit form" */
            [data-testid="InputInstructions"] {
                display: none !important;
            }
            /* Esconde o "olho" nativo do navegador (Edge/Windows) para não duplicar */
            input[type="password"]::-ms-reveal,
            input[type="password"]::-ms-clear {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🎓 EduTrack AI")
    st.subheader("🔑 Acesso Restrito")
    st.write("Faça login com sua conta acadêmica para acessar o painel.")
    
    with st.form("login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submit_btn = st.form_submit_button("Entrar no Sistema")
        
        if submit_btn:
            try:
                auth_url = f"{XANO_BASE_URL}/auth/login"
                
                # TESTE 1: Log de envio
                print(f"\n[DEBUG] Enviando requisição para: {auth_url}")
                print(f"[DEBUG] Dados enviados: {{'email': '{email}', 'password': '******'}}")
                
                response = requests.post(auth_url, json={"email": email, "password": password})
                
                # TESTE 2: Log de resposta
                print(f"[DEBUG] Status Code do Xano: {response.status_code}")
                print(f"[DEBUG] Resposta completa: {response.json()}")
                
                if response.status_code == 200:
                    st.session_state.auth_token = response.json().get("authToken")
                    st.success("Login realizado com sucesso! Carregando...")
                    st.rerun()
                else:
                    st.error("Acesso Negado. E-mail ou senha incorretos.")
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")
                print(f"[DEBUG] Erro de exceção: {e}")

# ---------------------------------------------------------
# GERENCIADOR DE NAVEGAÇÃO
# ---------------------------------------------------------

if not st.session_state.auth_token:
    # SE NÃO ESTIVER LOGADO: 
    # Como não temos mais a pasta mágica 'pages', a barra lateral simplesmente NÃO EXISTE no primeiro acesso.
    pagina_login = st.Page(tela_login, title="Login", icon="🔒")
    pg = st.navigation([pagina_login])
    pg.run()

else:
    # SE ESTIVER LOGADO: 
    # Revelamos o menu lateral e chamamos os arquivos da nova pasta 'telas'
    st.sidebar.header("Painel de Controle")
    if st.sidebar.button("Sair (Logout)"):
        st.session_state.auth_token = ""
        st.rerun()
        
    # Apontando para a nova pasta 'telas'
    dashboard = st.Page("telas/01_📚_Disciplinas.py", title="Disciplinas", icon="📚")
    tarefas = st.Page("telas/02_📝_Tarefas.py", title="Tarefas", icon="📝")
    perfil = st.Page("telas/03_👤_Perfil.py", title="Perfil", icon="👤")
    
    # Executa a navegação completa
    pg = st.navigation([dashboard, tarefas, perfil])
    pg.run()