import streamlit as st

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

# ---------------------------------------------------------
# DADOS
# ---------------------------------------------------------
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
# FILTROS
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    filtro_dia = st.selectbox("Filtrar por Dia:", ["Todos", "Segunda", "Terça", "Quarta", "Quinta"])

with col2:
    lista_disciplinas = ["Todas"] + sorted(list(set([aula["disciplina"] for aula in grade_horaria])))
    filtro_disciplina = st.selectbox("Filtrar por Disciplina:", lista_disciplinas)

st.markdown("---")

# ---------------------------------------------------------
# 1. RENDERIZA OS HORÁRIOS DA MATÉRIA
# ---------------------------------------------------------
for aula in grade_horaria:
    if filtro_dia != "Todos" and aula["dia"] != filtro_dia:
        continue
    if filtro_disciplina != "Todas" and aula["disciplina"] != filtro_disciplina:
        continue

    with st.container():
        st.subheader(f"📅 {aula['dia']} | ⏰ {aula['horario']}")
        st.markdown(f"**📖 Disciplina:** {aula['disciplina']}")
        st.markdown(f"**👨‍🏫 Prof(a):** {aula['prof']}")
        st.markdown(f"**📍 Sala:** {aula['sala']}")
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