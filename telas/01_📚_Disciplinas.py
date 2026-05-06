import streamlit as st
import requests
import os

# ---------------------------------------------------------
# TRAVA DE SEGURANÇA
# ---------------------------------------------------------
if "auth_token" not in st.session_state or not st.session_state.auth_token:
    st.warning("⚠️ Acesso negado. Por favor, faça login na página principal.")
    st.stop()

# ---------------------------------------------------------
# INTERFACE DA PÁGINA
# ---------------------------------------------------------
st.title("📚 Minha Grade e Horários")

# Configurações da API Xano
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti")

# ---------------------------------------------------------
# FORMULÁRIO DE CRIAÇÃO DE DISCIPLINA
# ---------------------------------------------------------
with st.expander("➕ Adicionar Nova Disciplina", expanded=False):
    st.markdown("Preencha os campos abaixo para criar uma nova disciplina:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nome_disciplina = st.text_input("Nome da Disciplina", placeholder="Ex: Python Avançado")
    
    with col2:
        professor = st.text_input("Professor(a)", placeholder="Ex: João Silva")
    
    with col3:
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        dia_selecionado = st.selectbox("Dia da Semana", dias_semana)
    
    if st.button("✅ Criar Disciplina", type="primary"):
        if nome_disciplina and professor and dia_selecionado:
            try:
                # Chamada à API POST do Xano
                api_url = f"{XANO_BASE_URL}/subjects"
                headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
                payload = {
                    "name": nome_disciplina,
                    "professor": professor,
                    "day_of_week": dia_selecionado
                }
                
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    st.success(f"✅ Disciplina '{nome_disciplina}' criada com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Erro ao criar disciplina: {response.json()}")
            except Exception as e:
                st.error(f"❌ Erro na conexão: {e}")
        else:
            st.warning("⚠️ Preencha todos os campos para criar uma disciplina.")

st.markdown("---")

# ---------------------------------------------------------
# BUSCAR DISCIPLINAS DO XANO
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def buscar_disciplinas():
    try:
        api_url = f"{XANO_BASE_URL}/subjects"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            disciplinas = response.json()
            if isinstance(disciplinas, list):
                return disciplinas
    except:
        pass
    return []

# Buscar disciplinas criadas pelo usuário
disciplinas_usuario = buscar_disciplinas()

# Se não houver disciplinas do usuário, usar dados estáticos
if not disciplinas_usuario:
    grade_horaria = [
        {"dia": "Segunda", "horario": "19h às 20h40 (Aula 1 e 2)", "disciplina": "SQL Fundamentals", "prof": "Evandro Victor Rocha Deliberal", "sala": "Lab 202 Paraíso"},
        {"dia": "Segunda", "horario": "21h às 22h40 (Aula 3 e 4)", "disciplina": "Software Engineering", "prof": "Mariana Moralles Rizzo", "sala": "108 Paraíso"},
        {"dia": "Terça", "horario": "19h às 20h40 (Aula 1 e 2)", "disciplina": "Database Design", "prof": "João Roberto Peres Ortega", "sala": "207 Paraíso"},
        {"dia": "Terça", "horario": "21h às 22h40 (Aula 3 e 4)", "disciplina": "Programming & Algorithms", "prof": "Odair Gabriel da Silva", "sala": "207 Paraíso"},
        {"dia": "Quarta", "horario": "19h às 20h40 (Aula 1 e 2)", "disciplina": "Innovation Lab: Advanced No/Low Code", "prof": "Leonardo Bontempo", "sala": "Lab 203 Paraíso"},
        {"dia": "Quarta", "horario": "21h às 22h40 (Aula 3 e 4)", "disciplina": "Database Design", "prof": "João Roberto Peres Ortega", "sala": "207 Paraíso"},
        {"dia": "Quinta", "horario": "19h às 20h40 (Aula 1 e 2)", "disciplina": "Programming & Algorithms", "prof": "Odair Gabriel da Silva", "sala": "Lab 201 Paraíso"},
        {"dia": "Quinta", "horario": "21h às 22h40 (Aula 3 e 4)", "disciplina": "SQL Fundamentals", "prof": "Evandro Victor Rocha Deliberal", "sala": "Lab 202 Paraíso"},
    ]
else:
    # Converter disciplinas do Xano para o formato da página
    grade_horaria = []
    for disc in disciplinas_usuario:
        grade_horaria.append({
            "id": disc.get("id"),
            "dia": disc.get("day_of_week", "N/A"),
            "horario": "A definir",
            "disciplina": disc.get("name", "Sem nome"),
            "prof": disc.get("professor", "N/A"),
            "sala": "N/A"
        })

# Banco de tarefas geral com a chave "disciplina" para o sistema filtrar sozinho
disc_inno = "Innovation Lab: Advanced No/Low Code"

tarefas_gerais = [
    {"id": 1, "titulo": "Configuração do Ambiente", "disciplina": disc_inno, "prazo": "20/02/2026", "status": "Concluída"},
    {"id": 2, "titulo": "Modelagem de Banco de Dados (DER)", "disciplina": disc_inno, "prazo": "25/02/2026", "status": "Concluída"},
    {"id": 3, "titulo": "Criação de Tabelas SQL (DDL)", "disciplina": disc_inno, "prazo": "02/03/2026", "status": "Concluída"},
    {"id": 4, "titulo": "Inserção de Dados (Sistema Restaurante)", "disciplina": disc_inno, "prazo": "05/03/2026", "status": "Concluída"},
    {"id": 5, "titulo": "Consultas SQL Otimizadas", "disciplina": disc_inno, "prazo": "08/03/2026", "status": "Concluída"},
    {"id": 6, "titulo": "Clone de Repositório e Branches (Git)", "disciplina": disc_inno, "prazo": "10/03/2026", "status": "Concluída"},
    {"id": 7, "titulo": "Configuração Streamlit e GitHub Workflows", "disciplina": disc_inno, "prazo": "11/03/2026", "status": "Concluída"},
    {"id": 8, "titulo": "Instalação de Dependências (npm/pip)", "disciplina": disc_inno, "prazo": "15/03/2026", "status": "Concluída"},
    {"id": 9, "titulo": "Estruturação da Interface no Streamlit", "disciplina": disc_inno, "prazo": "20/03/2026", "status": "Concluída"},
    {"id": 10, "titulo": "Conexão com API do Xano via Requests", "disciplina": disc_inno, "prazo": "25/03/2026", "status": "Concluída"},
    {"id": 11, "titulo": "Sistema de Autenticação e Login", "disciplina": disc_inno, "prazo": "05/04/2026", "status": "Concluída"},
    {"id": 12, "titulo": "Ocultar Menu Lateral com CSS/Navigation", "disciplina": disc_inno, "prazo": "15/04/2026", "status": "Concluída"},
    {"id": 13, "titulo": "Bloqueio de Rotas", "disciplina": disc_inno, "prazo": "25/04/2026", "status": "Concluída"},
    {"id": 14, "titulo": "Refatoração e Entrega Final", "disciplina": disc_inno, "prazo": "01/05/2026", "status": "Concluída"},
]

# ---------------------------------------------------------
# DADOS
# ---------------------------------------------------------
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    filtro_dia = st.selectbox("Filtrar por Dia:", ["Todos", "Segunda", "Terça", "Quarta", "Quinta"])

with col2:
    lista_disciplinas = ["Todas"] + sorted(list(set([aula["disciplina"] for aula in grade_horaria])))
    filtro_disciplina = st.selectbox("Filtrar por Disciplina:", lista_disciplinas)

st.markdown("---")

# ---------------------------------------------------------
# FUNÇÃO DE DELETAR DISCIPLINA
# ---------------------------------------------------------
def deletar_disciplina(disciplina_id):
    try:
        api_url = f"{XANO_BASE_URL}/subjects/{disciplina_id}"
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.delete(api_url, headers=headers)
        
        if response.status_code == 200:
            st.success(f"✅ Disciplina deletada com sucesso!")
            st.session_state.clear()
            st.rerun()
        else:
            st.error(f"❌ Erro ao deletar disciplina: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Erro na conexão: {e}")

# ---------------------------------------------------------
# 1. RENDERIZA OS HORÁRIOS DA MATÉRIA
# ---------------------------------------------------------
for aula in grade_horaria:
    if filtro_dia != "Todos" and aula["dia"] != filtro_dia:
        continue
    if filtro_disciplina != "Todas" and aula["disciplina"] != filtro_disciplina:
        continue

    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader(f"📅 {aula['dia']} | ⏰ {aula['horario']}")
            st.markdown(f"**📖 Disciplina:** {aula['disciplina']}")
            st.markdown(f"**👨‍🏫 Prof(a):** {aula['prof']}")
            st.markdown(f"**📍 Sala:** {aula['sala']}")
        
        with col2:
            if "id" in aula and aula["id"]:
                if st.button("🗑️ Deletar", key=f"delete_{aula['id']}"):
                    deletar_disciplina(aula["id"])
        
        st.markdown("---")

# ---------------------------------------------------------
# 2. RENDERIZA AS TAREFAS VINCULADAS (Apenas Visualização)
# ---------------------------------------------------------
if filtro_disciplina != "Todas":
    # O sistema busca na lista de tarefas quais pertencem à disciplina selecionada
    tarefas_da_disciplina = [t for t in tarefas_gerais if t["disciplina"] == filtro_disciplina]
    
    # Se ele encontrar alguma tarefa para esta matéria, ele desenha o bloco
    if len(tarefas_da_disciplina) > 0:
        st.subheader("📝 Tarefas Vinculadas (Leitura)")
        st.info("💡 Apenas visualização. Acesse o menu 'Tarefas' na barra lateral para interagir ou alterar o status.")
        
        for t in tarefas_da_disciplina:
            with st.expander(f"📌 Tarefa {t['id']:02d}: {t['titulo']}"):
                st.write(f"**Prazo:** {t['prazo']}")
                # Apenas texto visual, sem checkbox!
                st.write(f"**Status Atual:** ✅ {t['status']}")