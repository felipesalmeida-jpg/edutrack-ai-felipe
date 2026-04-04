import streamlit as st
import requests
import os

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="EduTrack AI", page_icon="🎓")

# Título Principal
st.title("🎓 EduTrack AI")

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")

# Inicializa o estado de autenticação na sessão
if "auth_token" not in st.session_state:
    st.session_state.auth_token = os.getenv("XANO_AUTH_TOKEN", "")

# Fluxo de Login
if not st.session_state.auth_token:
    st.subheader("🔑 Login")
    st.write("Por favor, acesse com suas credenciais para gerenciar suas disciplinas.")
    
    with st.form("login_form"):
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        submit_btn = st.form_submit_button("Entrar")
        
        if submit_btn:
            try:
                # Utilizamos a rota padrão de auth do Xano
                auth_url = f"{XANO_BASE_URL}/auth/login"
                response = requests.post(auth_url, json={"email": email, "password": password})
                
                if response.status_code == 200:
                    st.session_state.auth_token = response.json().get("authToken")
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas. Verifique seu e-mail e senha.")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")

# Fluxo da Aplicação Autenticada
else:
    # Sidebar (Menu Lateral)
    st.sidebar.header("Menu")
    menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])
    
    if st.sidebar.button("Sair (Logout)"):
        st.session_state.auth_token = ""
        st.rerun()

    # Conteúdo Dinâmico
    if menu_option == "Dashboard":
        st.write("Bem-vindo ao seu assistente acadêmico!")
        st.info("Conecte ao Xano para ver seus dados reais.")
        
        # Exemplo de Métrica Visual
        col1, col2 = st.columns(2)
        col1.metric("Disciplinas Ativas", "0")
        col2.metric("Tarefas Pendentes", "0")

    elif menu_option == "Disciplinas":
        st.subheader("📚 Minhas Disciplinas")
        
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        try:
            response = requests.get(f"{XANO_BASE_URL}/subjects", headers=headers)
            
            if response.status_code == 200:
                subjects = response.json()
                if not subjects:
                    st.info("Você ainda não tem disciplinas cadastradas.")
                for subject in subjects:
                    with st.container(border=True):
                        st.markdown(f"#### {subject.get('name')} ({subject.get('semester', 'N/A')})")
                        st.write(f"**Descrição:** {subject.get('description', 'Sem descrição')}")
                        st.write(f"**Status:** {subject.get('status')} | **Créditos:** {subject.get('credits')}")
            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erro de conexão com o backend: {e}")

    elif menu_option == "Tarefas":
        st.subheader("Gerenciamento de Tarefas")
        st.info("Módulo em construção. Em breve você poderá adicionar tarefas relacionadas às disciplinas!")